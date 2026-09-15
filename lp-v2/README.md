# LP Blue Bolt Agency — layout da Blue Bolt AI

Duplicado da landing page da **Blue Bolt AI** com o design intacto — mesmas
fontes, cores, efeitos e animações — mas a vender a **Blue Bolt Agency**
(Sistema Previsível de Aquisição de Clientes). Leva a VSL a cavalo entre a
primeira e a segunda dobra.

## Ver a página

```bash
cd lp-v2 && python3 -m http.server 8000
# abrir http://localhost:8000
```

## Como foi feito

O `index.html` é **gerado**: o `build.py` parte de `source/bluebolt-ai-ads.html`
(o original, intocado) e troca só o conteúdo. Nenhuma regra de CSS do original
foi alterada — só foi acrescentado o bloco da VSL no fim do `<style>`. Cada
substituição confirma quantas ocorrências esperava encontrar, por isso uma
alteração no original que parta o script dá erro em vez de passar despercebida.

```bash
python3 build.py     # reescreve index.html a partir do original
```

Para mudar a copy, edita-se o `build.py`, não o `index.html`.

## Sem barra de menu

A barra fixa do topo foi removida — marcação e JS. Numa página de anúncios só
oferecia saídas, e além disso tapava o título do hero. O CTA que lá vivia
("Diagnóstico gratuito") já existe no hero e repete-se no fim da página. As
regras de CSS do `#nav` ficaram na folha, por não se mexer no CSS original;
não têm efeito nenhum.

## A secção do Ricardo

`#autoridade` ficou **palavra por palavra** como estava, incluindo o título
"Quem está por trás da Blue Bolt AI", o cargo "Cofundador da Blue Bolt AI" e as
duas frases sobre IA. Foi pedido assim. Se um dia quiser adaptá-la à agência,
são as únicas três menções a "Blue Bolt AI" que sobraram na página.

## A VSL

Vídeo do YouTube `v4o2YB1vPjI` — o VSL da Blue Bolt, o mesmo da LP do Elementor.
Fica a cavalo entre as duas dobras com a mesma técnica da LP de referência: o
hero ganha folga em baixo, o bloco do vídeo sobe com margem negativa em cima e
em baixo, e a secção seguinte ganha folga em cima. Medido no browser: 216px dos
438px de altura ficam sobre o hero — praticamente a meio.

Em vez de um `<iframe>` sempre carregado, o player mostra a capa e só insere o
iframe ao clicar. Fica igual à vista, mas a página não arrasta o YouTube em cada
visita — numa LP de anúncios isso conta.

## Imagens

A página de IA não está online, por isso três ficheiros não puderam ser
recuperados e foram substituídos por equivalentes do repositório:

| Original | Substituto | Nota |
| --- | --- | --- |
| `ricardo.webp` | `img/ricardo.avif` | Retrato do Ricardo da secção de equipa |
| `bluebolt-logo.webp` | `img/bluebolt-logo.webp` | Logótipo Blue Bolt |
| `bluebolt-ai-brand.png` | `img/equipa.webp` | A foto do robô era da oferta de IA; entra a foto da equipa |

Se enviar os ficheiros originais, é só substituí-los em `img/` com os mesmos
nomes.

## Por ligar antes de publicar

- **O formulário não envia nada.** O `handleLeadSubmit` mostra a mensagem de
  obrigado e descarta os dados — é assim no original ("placeholder — sem backend
  ligado"). Numa página de anúncios isto significa perder todas as leads.
- **Os IDs de tracking são placeholders**: `GA_MEASUREMENT_ID`,
  `META_PIXEL_ID` e `GOOGLE_SITE_VERIFICATION_CODE`.
- **`robots` está em `noindex, nofollow`**, herdado do original.
- O conteúdo é servido do Google Fonts (Manrope e Inter) e do cdnjs (GSAP),
  como no original. A Archia é auto-alojada.
