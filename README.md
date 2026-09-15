# LP Blue Bolt Agency — versão HTML estática

Landing page "Sessão Estratégica" convertida do export JSON do Elementor
(WordPress) para HTML, CSS e JavaScript puros. Não precisa de WordPress, de PHP
nem de ligação à internet: são ficheiros estáticos que podem ser servidos por
qualquer alojamento, CDN ou GitHub Pages.

## Ver a página

```bash
python3 -m http.server 8000   # ou: npx serve .
# abrir http://localhost:8000
```

Abrir o `index.html` directamente com `file://` também funciona, com a excepção
do envio do formulário (o `fetch` para o webhook é bloqueado pelo CORS nessa
origem).

## Estrutura

```
index.html                     página gerada
assets/css/base.css            sistema de layout (escrito à mão)
assets/css/page.css            estilos por elemento (gerado)
assets/css/fonts.css           @font-face das fontes auto-alojadas (gerado)
assets/js/app.js               carrossel, acordeão, modal, formulário, vídeo
assets/img/                    68 imagens e o vídeo de fundo, descarregados do WP
assets/fonts/                  DM Sans e Instrument Serif em woff2
assets/icons/                  ícones Font Awesome em SVG
tools/elementor_to_html.py     conversor JSON → HTML/CSS
tools/fetch_assets.py          descarrega imagens e fontes, escreve o asset-map
tools/page.template.html       molde do documento (head, metas, scripts)
tools/source/                  export do Elementor + metadados dos vídeos
```

## Regenerar

O `index.html`, o `page.css` e o `fonts.css` são gerados — as edições à mão
perdem-se. Para alterar conteúdo, mexer no export e voltar a correr:

```bash
python3 tools/fetch_assets.py       # só quando há imagens ou fontes novas
python3 tools/elementor_to_html.py  # reescreve index.html e page.css
```

O `base.css`, o `app.js` e o `page.template.html` são escritos à mão e podem ser
editados livremente.

### Como funciona o conversor

Percorre a árvore do export e, para cada elemento, emite uma `<div>` com a
classe `e-<id>` (o mesmo id do Elementor) e as respectivas regras CSS. Mantém os
dois *breakpoints* que o site original tinha activos — tablet (≤1024px) e
telemóvel (≤767px) — e replica os comportamentos que o runtime do Elementor
aplicava por omissão abaixo dos 767px: largura de container de volta a 100%,
`flex-wrap: wrap` nas linhas e grelhas reduzidas a uma coluna.

O `custom_css` de cada widget é preservado: os blocos que usam a palavra-chave
`selector` ficam ligados ao elemento certo; os blocos globais (como
`.instrument-serif-regular` ou `.text-gradient`) são deduplicados e emitidos uma
só vez.

## O que substituiu os widgets do Elementor Pro

| Widget original | Substituição |
| --- | --- |
| `nested-carousel` (5×) | carrossel em JS puro, com setas, arrasto e teclado |
| `nested-accordion` | `<details>`/`<summary>` nativos |
| `off-canvas` | modal acessível (foco, `Esc`, clique no fundo) |
| `form` | `<form>` com validação nativa e `POST` JSON para o webhook Pabbly |
| `presto_video` / `[presto_player]` | *facade* do YouTube: carrega o iframe só ao clicar |
| ícones Font Awesome | SVG embutido com `fill="currentColor"` |

Os dez vídeos eram servidos pelo plugin Presto Player, que não vem no export.
Os IDs do YouTube e as capas foram recuperados da página publicada e estão em
`tools/source/presto-videos.json` — a ordem segue a ordem dos widgets na página
(primeiro o VSL, depois os nove testemunhos).

## Decisões que se afastam do original

Poucas, e todas deliberadas:

- **Fontes auto-alojadas.** A DM Sans e a Instrument Serif deixaram de vir do
  Google Fonts e passaram a `assets/fonts/`. A página deixa de fazer pedidos a
  terceiros e de depender do consentimento de cookies para renderizar texto.
- **Variáveis CSS em falta.** O bloco HTML do funil usa `--bord`, `--bord-b`,
  `--bg2` e `--sans`, que no site original nunca chegaram a ser definidas (vinham
  de uma folha do tema que não está no export), pelo que as margens e os fundos
  desse bloco simplesmente não apareciam. Ficaram definidas em `base.css` com
  valores neutros para a secção branca onde o bloco vive.
- **`max-width: 100%` nos containers.** O Elementor deixa containers com largura
  fixa transbordarem em ecrãs estreitos; aqui ficam limitados, para não haver
  scroll horizontal.
- **Grelha de 4 colunas a duas em tablet.** O export não traz valor de tablet
  para a secção dos pilares, e manter as quatro colunas entre 768px e 1024px
  fazia o conteúdo transbordar a janela. Passa a duas colunas nessa faixa.
- **Um `<h1>`.** O export não tinha nenhum (o tema do WordPress é que punha o
  título da página). O primeiro título passou a `<h1>`; os restantes mantêm-se.
- **Vídeos só carregam ao clique.** Em vez de dez players a inicializar no
  arranque, cada vídeo mostra a capa e só insere o iframe quando é pedido.

## A corrigir no conteúdo (herdado do original)

Não foram alterados, para a conversão ficar fiel ao export, mas valem uma
revisão:

- O campo de email do formulário tem a etiqueta e o *placeholder* trocados —
  etiqueta `exemplo@email.com`, *placeholder* `Email`.
- O botão de WhatsApp aponta para `https://wa.me/351`, que só tem o indicativo
  do país e nenhum número.
- O endereço do webhook do formulário está no HTML (`data-webhook`), tal como
  estava no formulário do Elementor. Sendo um endpoint público de recepção, quem
  vir o código consegue enviar-lhe dados; se isso for um problema, vale a pena
  pô-lo atrás de uma função sem servidor.

## Créditos

Ícones da Font Awesome Free 6.5.2 (CC BY 4.0). Tipos de letra DM Sans e
Instrument Serif (SIL Open Font License 1.1).
