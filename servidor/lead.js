/* Recebe a submissão do formulário da landing page e faz duas coisas:
   manda o evento para a Conversions API do Meta e devolve a lead a quem
   a tem de receber.

   PORQUE É QUE ISTO NÃO VIVE NA PÁGINA
   O token da Conversions API é uma credencial de servidor. Quem o tiver
   pode escrever conversões na conta de anúncios da Blue Bolt e estragar
   a otimização das campanhas. Não entra no HTML, não entra neste
   repositório (que é público) e não entra no histórico do Git: vem de uma
   variável de ambiente, definida no painel de quem alojar isto.

   COMO CORRER
   É um handler de `fetch` padrão. Serve tal e qual em Cloudflare Workers
   e em Netlify Functions v2. Na Vercel, trocar a última linha por
   `export const config = { runtime: 'edge' }` e `export default handler`.

   VARIÁVEIS DE AMBIENTE
     META_PIXEL_ID     260575891666892
     META_CAPI_TOKEN   o token (NUNCA aqui dentro)
     META_TEST_CODE    opcional, o código de teste do Events Manager
     ORIGEM_PERMITIDA  https://blueboltai.github.io  (ou o domínio final)
*/

const VERSAO_API = 'v21.0';

/* O Meta exige os dados pessoais em SHA-256, normalizados primeiro:
   sem espaços à volta e em minúsculas. Um email com maiúsculas e outro
   sem elas têm de dar o mesmo hash, senão a correspondência falha. */
async function hash(valor) {
  if (!valor) return undefined;
  const limpo = String(valor).trim().toLowerCase();
  if (!limpo) return undefined;
  const bytes = new TextEncoder().encode(limpo);
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(digest)].map(b => b.toString(16).padStart(2, '0')).join('');
}

/* O telefone vai só com dígitos, com indicativo e sem o +. Um número
   escrito "927 135 702" e outro "+351927135702" são a mesma pessoa. */
async function hashTelefone(valor) {
  if (!valor) return undefined;
  let d = String(valor).replace(/\D/g, '');
  if (!d) return undefined;
  if (d.length === 9 && /^9|^2/.test(d)) d = '351' + d;   // número português sem indicativo
  return hash(d);
}

export default async function handler(pedido, env = globalThis.process?.env ?? {}) {
  const origem = env.ORIGEM_PERMITIDA || '*';
  const cabecalhos = {
    'Access-Control-Allow-Origin': origem,
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json',
  };

  if (pedido.method === 'OPTIONS') return new Response(null, { status: 204, headers: cabecalhos });
  if (pedido.method !== 'POST') {
    return new Response(JSON.stringify({ erro: 'só POST' }), { status: 405, headers: cabecalhos });
  }

  let dados;
  try { dados = await pedido.json(); }
  catch { return new Response(JSON.stringify({ erro: 'corpo inválido' }), { status: 400, headers: cabecalhos }); }

  /* O mínimo para a lead servir para alguma coisa. */
  if (!dados.email && !dados.telefone) {
    return new Response(JSON.stringify({ erro: 'faltam email e telefone' }), { status: 400, headers: cabecalhos });
  }

  const pixel = env.META_PIXEL_ID;
  const token = env.META_CAPI_TOKEN;
  if (!pixel || !token) {
    /* Sem credenciais não se finge que correu bem: a lead ainda assim
       não se perde, mas quem chamou fica a saber que o Meta não soube. */
    console.error('META_PIXEL_ID ou META_CAPI_TOKEN por definir');
    return new Response(JSON.stringify({ ok: false, erro: 'servidor mal configurado' }), { status: 500, headers: cabecalhos });
  }

  const evento = {
    event_name: 'Lead',
    event_time: Math.floor(Date.now() / 1000),
    /* O mesmo identificador que o browser usou. É por ele que o Meta
       percebe que os dois eventos são um só, em vez de contar a lead
       duas vezes. Sem isto, a CAPI duplica tudo o que o pixel já mandou. */
    event_id: dados.event_id || undefined,
    action_source: 'website',
    event_source_url: dados.pagina || undefined,
    user_data: {
      em: await hash(dados.email),
      ph: await hashTelefone(dados.telefone),
      fn: await hash((dados.nome || '').split(' ')[0]),
      ln: await hash((dados.nome || '').split(' ').slice(1).join(' ')),
      /* Não são hashados: o Meta usa-os como estão. São o que mais
         melhora a correspondência, e vêm dos cookies do pixel. */
      fbp: dados.fbp || undefined,
      fbc: dados.fbc || undefined,
      client_ip_address: pedido.headers.get('x-forwarded-for')?.split(',')[0].trim()
                      || pedido.headers.get('cf-connecting-ip') || undefined,
      client_user_agent: pedido.headers.get('user-agent') || undefined,
    },
    custom_data: {
      content_name: 'Diagnóstico gratuito de 30 minutos',
      content_category: 'formulario',
    },
  };

  /* Fora as chaves vazias: o Meta rejeita campos a `undefined`. */
  evento.user_data = Object.fromEntries(Object.entries(evento.user_data).filter(([, v]) => v));

  const corpo = { data: [evento], access_token: token };
  if (env.META_TEST_CODE) corpo.test_event_code = env.META_TEST_CODE;

  let resultadoMeta;
  try {
    const r = await fetch(`https://graph.facebook.com/${VERSAO_API}/${pixel}/events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo),
    });
    resultadoMeta = await r.json();
    if (!r.ok) console.error('CAPI recusou:', JSON.stringify(resultadoMeta));
  } catch (e) {
    console.error('CAPI inacessível:', e.message);
  }

  /* ─────────────────────────────────────────────────────────────
     POR LIGAR: o destino da lead.
     Sem isto, o evento chega ao Meta mas os dados da pessoa não vão
     para lado nenhum — que é exatamente o problema que este ficheiro
     existe para resolver. Escolher um:
       • email para geral@bluebolt.pt (Resend, Postmark, SendGrid)
       • uma linha numa folha do Google
       • o CRM, se já houver um
     ───────────────────────────────────────────────────────────── */
  console.log('LEAD', JSON.stringify({
    nome: dados.nome, email: dados.email, telefone: dados.telefone,
    empresa: dados.empresa, pagina: dados.pagina,
  }));

  return new Response(JSON.stringify({ ok: true, meta: resultadoMeta?.events_received ?? null }), {
    status: 200, headers: cabecalhos,
  });
}

/* Cloudflare Workers */
export const fetchHandler = { fetch: (req, env) => handler(req, env) };
