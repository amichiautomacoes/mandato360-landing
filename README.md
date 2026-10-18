# Landing MANDATO 360

Landing Flask com duas rotas, sem banco de dados ou autenticação:

- `/`: landing page reconstruída com HTML semântico e conteúdo de `content.json`.
- `/dashboard`: página com o botão **Ir para o dashboard**, apontando para `http://localhost:8501`.

## Deploy no EasyPanel

O repositório contém a aplicação na raiz, com `Dockerfile` pronto para build no
próprio EasyPanel. Não é necessário executar Docker na máquina local.

1. Crie um serviço **App** e selecione a origem **GitHub**.
2. Informe o repositório `amichiautomacoes/mandato360-landing`, branch `main`.
3. Defina **Build Path** como `/` e o builder como **Dockerfile**, caminho `Dockerfile`.
4. Configure o domínio para a porta interna **8501** usando HTTP no container.
5. Clique em **Deploy**. O EasyPanel constrói a imagem e inicia o serviço.

O container executa Gunicorn em `0.0.0.0:8501`, com dois workers e quatro threads
por worker, sem modo debug e com usuário sem privilégios de root. O healthcheck
consulta `/` a cada 30 segundos; os logs são enviados para a saída do container.
Não são necessários volumes, banco de dados ou variáveis de ambiente para a landing.

O `.env` local serve somente para autenticar o envio ao GitHub. Ele fica fora
do Git e do contexto de build por meio de `.gitignore` e `.dockerignore`.
As credenciais Git não precisam ser cadastradas como variáveis da aplicação.

Referências: [serviços App](https://easypanel.io/docs/services/app) e
[build com Dockerfile](https://easypanel.io/docs/builders).

## Instalar

No PowerShell, a partir da pasta `Lpaas`, ative a venv já criada e entre em `landing`:

```powershell
.\.venv\Scripts\Activate.ps1
cd landing
pip install -r requirements.txt
```

As dependências de produção são Flask e Gunicorn. No Windows, a instalação
ignora o Gunicorn; o servidor de desenvolvimento continua disponível com Flask.

## Rodar

Dentro de `landing`, com a venv ativa:

```powershell
python app.py
```

Abra <http://127.0.0.1:5000>. O Flask roda na porta `5000` com `debug=True`.
Encerre o servidor com `Ctrl+C`.

## Apontar para o dashboard Streamlit

Altere a constante `DASHBOARD_URL` em `app.py`:

```python
DASHBOARD_URL = "http://localhost:8501"
```

A rota `/dashboard` mostra o botão **Ir para o dashboard** com esse endereço.
O Streamlit deve ser iniciado separadamente. Os botões **Fale Conosco** da landing
abrem o WhatsApp em uma nova aba. O texto e o destino ficam em `contact_button.label`
e `contact_button.url` no `content.json`; o link atual é `https://wa.me/5531975564544`.

## Estrutura

```text
landing/
├── Dockerfile
├── .dockerignore
├── .gitignore
├── app.py
├── content.json
├── requirements.txt
├── README.md
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   ├── fonts/
│   └── img/
├── templates/
│   ├── _image.html
│   ├── index.html
│   └── redirect.html
└── tools/
    ├── optimize_images.py
    └── prepare_hero_video.py
```

## Editar o conteúdo

Todos os textos das duas páginas vêm de `landing/content.json`, incluindo
títulos, parágrafos, botões, navegação, textos alternativos das imagens e
rótulos de acessibilidade. O `app.py` usa `json.load` em cada requisição e
passa o resultado ao template como `content`. Salve o JSON em UTF-8 e recarregue
a página para ver as alterações.

O JSON foi organizado a partir de `../output/content.json`. As descrições dos
três módulos que não estavam visíveis na captura foram recuperadas dos dados
incorporados em `../output/page.html`. Os botões de contato usam o WhatsApp
configurado no JSON. Os arquivos de captura permanecem em `output/`.

As seções seguem a ordem Hero, Solução, Público-alvo, CTA final e
Rodapé. As classes CSS usam nomes em português, como `hero-titulo`,
`secao-solucao`, `card-modulo` e `rodape`. Os IDs identificam os destinos das
âncoras da navegação.

## Assets e estilos

Os templates geram os caminhos de CSS, JavaScript e imagens com
`url_for('static', filename=...)`. O layout e a navegação são responsivos.
As imagens do hero estático aparecem com uma transição suave de opacidade e deslocamento ao
entrarem na tela, uma vez por imagem e após o carregamento. A animação usa
`IntersectionObserver` e respeita a preferência por movimento reduzido;
sem JavaScript ou suporte ao observador, as imagens ficam visíveis normalmente.

Todos os cards internos usam um gradiente azul discreto, definido em
`--gradiente-card`: de `#1a3452` a `#0e1e33`, passando por `#142a44`, a 145°.
O mesmo fundo é aplicado aos quatro módulos da seção 2 e aos cards de público-alvo
da seção 3, tanto no celular quanto no desktop. Os textos usam cores claras para
preservar a leitura. Os arquivos decorativos antigos permanecem em `static/img/`.

Os quatro cards ocupam a largura da grade para apresentar os dashboards.
Os textos descritivos aparecem logo abaixo do título de cada card, antes das imagens.
O RaioX Territorial usa
as capturas reais `raioxestado.png`, `raioxbairro.png` e `raioxconcentracao.png`.
O carrossel combina Coverflow 3D com máscaras `clip-path`: a captura central
fica inteira, sem blur, enquanto as laterais usam perspectiva, escala e
opacidade menores. Deslocamento e revelação compartilham uma animação de
700 ms, com inclinação lateral discreta de 14°; a terceira imagem cruza por trás ao trocar de lado, inclusive na volta
da última para a primeira. As proporções originais são preservadas, sem cortes.

O clique nas prévias laterais, as teclas de direção, Home/End, o arraste com mouse
e o swipe no celular permitem navegar, sem reprodução automática. Não há legendas,
contadores, setas ou indicadores visíveis abaixo das imagens no desktop; a posição continua
disponível para leitores de tela. O arraste não
abre a imagem por engano. A preferência por movimento reduzido elimina a animação, e sem
JavaScript as imagens continuam acessíveis por rolagem horizontal. As capturas
são carregadas sob demanda, com WebP de alta qualidade em 480, 800 e largura
original, mantendo os PNGs como fallback. Configurações, legendas e textos
alternativos ficam em `solution.modules[0].gallery`. O componente está em
`templates/_carousel.html` e `static/js/carousel.js`.

Clicar na captura central abre um lightbox compartilhado pelos quatro cards,
implementado em `templates/_lightbox.html` e `static/js/lightbox.js`. Ele usa o PNG
original, com a imagem inteira ajustada à tela, zoom de até 8× e deslocamento por
arraste com mouse ou rolagem nativa no celular. Os botões e as teclas +, − e 0
controlam o zoom; Esc, o botão de fechar ou o fundo externo fecham a ampliação.
O diálogo mantém o foco no modal, bloqueia a rolagem da página e devolve o foco à
captura ao fechar. A preferência por movimento reduzido também desliga a entrada
animada do lightbox. Sem JavaScript ou suporte a diálogo, o link abre o PNG original.
Os textos do lightbox ficam em `lightbox` no JSON, e o rótulo de ampliação em
`solution.modules[].gallery.expand`.

O DNA do Eleitor usa o mesmo carrossel com `dna1.png`, `dna3.png` e `dna2.png`,
nessa ordem, configurado em `solution.modules[1].gallery`. A navegação de cada
carrossel é independente.

A DRE da Campanha usa `dre1 (1).png`, `dre2.png` e `dre3.png`, nessa ordem,
configurados em `solution.modules[2].gallery`. A primeira captura é copiada
para `static/img/dre1.png`.

O Impacto Político usa `forca1.png` e `forca2.png`, nessa ordem, configurados em
`solution.modules[3].gallery`. Com duas capturas, prévias decorativas da imagem
adjacente aparecem nas duas laterais, preservando a transição nos dois sentidos.
Essas cópias não acrescentam etapas nem indicadores e ficam ocultas dos leitores
de tela. O card mantém seu conteúdo textual e fundo.

Até 820 px, os quatro módulos exibem uma galeria exclusiva para celular, com
imagens verticais de 1080 × 1350 px (4:5). Cada captura ocupa toda a largura interna
do card, sem prévias laterais, cortes ou distorção. Os textos mantêm seus recuos.
O RaioX usa oito imagens de `../assets/raioxcel`; DNA, DRE e Impacto usam quatro
imagens de `../assets/Dnacel`, `../assets/drecel` e `../assets/impactocel`, respectivamente.
A ordem segue os nomes numéricos dos arquivos, de `1.png` em diante.

Os originais ficam em `static/img/mobile/<módulo>/`, e as versões WebP em
480, 800 e 1080 px ficam em `static/img/responsive/`. A configuração de cada
galeria está em `solution.modules[].gallery.mobile`, incluindo títulos e
textos alternativos. A navegação usa rolagem horizontal nativa com encaixe de
uma imagem por vez; setas discretas em SVG ficam sobre as laterais da imagem,
com alvos de 44 × 48 px. Não há texto de orientação nem contador visível abaixo
das capturas; a posição é anunciada para leitores de tela. As teclas de direção
e Home/End também navegam. O toque na imagem
abre o mesmo lightbox, usando o PNG vertical original.

O comportamento mobile está em `static/js/mobile-carousel.js` e respeita
movimento reduzido. Sem JavaScript, as imagens continuam acessíveis por deslize,
com uma seta de orientação estática. Acima de 820 px, permanecem as imagens
horizontais e o Coverflow original, com navegação independente da galeria mobile.

As seções de módulos (seção 2), público-alvo (seção 3) e chamada final (seção 4)
compartilham o fundo em CSS da seção 2: cor `#1c2c42` e grade de 56 × 56 px
a 28% de opacidade, suavizada nas extremidades. A classe `.secao-fundo` centraliza
esse visual em todas as larguras de tela. Os cards internos usam `--gradiente-card`,
e os textos corridos mantêm cores claras para leitura.

Para regenerar os WebP dos fundos, do carrossel ou da imagem alternativa do hero,
atualize os caminhos e dimensões em `section_background`, `audience.background`, `solution.card_background`,
`solution.modules[].gallery.slides[].image`,
`solution.modules[].gallery.mobile.slides[].image` ou `hero.image`
no JSON e execute na pasta `Lpaas`, com a venv que já contém Playwright:

```powershell
.\.venv\Scripts\python.exe landing\tools\optimize_images.py
```

Para regenerar apenas as versões WebP da galeria mobile, preservando todos os
arquivos de imagem do desktop, execute na pasta `Lpaas`:

```powershell
.\.venv\Scripts\python.exe landing\tools\optimize_images.py --mobile-only
```

O hero usa vídeos próprios para celular e desktop. O desktop foi preparado a
partir de `../assets/download.mp4`, horizontal 16:9, com cerca de oito segundos
no original. A abertura preta é removida e os últimos 0,6 segundo recebem uma
fusão com o início, criando uma emenda suave no loop sem apagar a imagem. O
arquivo preparado tem cerca de sete segundos. O celular usa
`../assets/fundocel.mp4`, vertical 9:16, com a mesma preparação do loop.
No desktop, o vídeo cobre todo o fundo da primeira seção com `object-fit: cover`.
Até 820 px, a seção divide o espaço em duas faixas de mesma altura: o texto e o
botão ficam na faixa superior e o mapa na inferior. O vídeo e sua capa usam
`object-fit: contain`, ancorados na base, para preservar a composição vertical.
A altura acompanha o conteúdo em telas pequenas e com texto ampliado, evitando
sobreposição com o mapa. Os vídeos mantêm a luminosidade original. A seção
ocupa pelo menos a altura disponível da tela abaixo do cabeçalho. O vídeo
inicia automaticamente, sem som, em loop, e
continua ao rolar a página, sem controles de reprodução visíveis. Ao trocar
de aba, a reprodução pausa e retoma automaticamente no retorno.

`hero.video` no JSON centraliza os arquivos, as dimensões e as capas. `poster`
define a capa do celular; `desktop_poster` define a composição horizontal, usada
acima de 820 px tanto no vídeo quanto no fallback `picture`.
As versões em `static/video/` usam H.264: 540 × 960 px e cerca de 314 KB para
celular, 1280 × 720 px e cerca de 1,03 MB para desktop, sem ampliar a resolução
do original. As capas WebP mantêm o
visual durante o carregamento, em caso de falha ou sem JavaScript. O vídeo
original é preservado. Para regenerar somente o desktop e sua capa, execute na
pasta `Lpaas`:

```powershell
.\.venv\Scripts\python.exe landing\tools\prepare_hero_video.py --target desktop
```

O destino padrão é `desktop`, para evitar substituir o vídeo vertical do celular
ao atualizar o original horizontal. Para regenerar o vídeo do celular e a capa
de 540 px, use:

```powershell
.\.venv\Scripts\python.exe landing\tools\prepare_hero_video.py --target mobile --source assets\fundocel.mp4
```

Os parâmetros `--trim-start`
e `--crossfade` ajustam, em segundos, o corte inicial e a duração da fusão.

Até 820 px, o menu pode ser aberto pelo botão **Menu** e fecha por seleção,
toque fora ou Escape. Seu estado também é ajustado ao redimensionar a tela.
Sem JavaScript, os links continuam visíveis no fluxo da página. O cabeçalho
recolhido mede 65 px, e as âncoras compensam sua altura real.

Em telas de até 560 px, os textos corridos usam 16 px, os textos auxiliares
usam ao menos 14 px e os títulos têm escala própria para celular. Links e
botões têm alvos de toque de pelo menos 44 × 44 px. Os botões do WhatsApp
ficam no menu e na seção final, sem elemento flutuante sobre o conteúdo.

Todos os arquivos de `../output/assets/` foram copiados com seus nomes originais:
fontes `.woff`, `.woff2`, `.ttf` e `.otf` ficam em `static/fonts/`; os demais
assets ficam em `static/img/`. As imagens adicionais dos módulos também ficam
em `static/img/`.

O `static/css/style.css` usa os valores de `../output/computed_styles.json`:
fundo `#090A0F`, texto `#F4F5F7`, texto secundário `#9BA1B0`, ciano `#00808F`,
azul `#3B82F6`, gradiente de seção a 160°, botões com raio de 4 px, sombra
das ações e blur de 12 px no cabeçalho. Os cards usam o gradiente azul opaco
definido em `--gradiente-card`.
As variáveis de `:root`, como `--cor-primaria`, `--fonte-corpo`,
`--fonte-titulo`, `--espaco-6` e `--gradiente-card`, permitem ajustar a identidade.

Os seletores genéricos de card, hero, btn e container e o seletor `h4` não
tinham elementos na extração. Esses componentes foram adaptados a partir de
`a`, `button`, `header`, `section`, grid e das variáveis do tema em `page.html`;
os raios dos cards e das imagens derivam do raio base dos botões.

Toda a interface usa **Montserrat**, com peso **400** nos textos, **700** nos
subtítulos, destaques e botões, e **900** nos títulos principais. Os `@font-face`
usam `font-display: swap` e as variantes Latin e Latin Extended, em dois arquivos
WOFF2 locais em `static/fonts/`. A fonte foi obtida do Google Fonts; a licença
está em `static/fonts/Montserrat-OFL.txt`, e o projeto original está no
[repositório Google Fonts](https://github.com/google/fonts/tree/main/ofl/montserrat).
Os caminhos são relativos ao CSS, sem chamadas a serviços externos de fontes.
Grid e Flexbox controlam o layout; os cards usam fundo opaco em todos os navegadores.

O fundo comum dos módulos é definido em `--gradiente-card`; os textos
continuam em `solution.modules`. Os caminhos das capturas são relativos à pasta
`static/`, por exemplo `img/mobile/raiox/1.png`.

## Boas práticas

- Código comentado em português e classes CSS com nomes em português.
- Imagens, SVGs, fontes, CSS e JavaScript locais, sem CDNs externas.
- JavaScript puro para menu mobile, rolagem de âncoras e entrada das imagens.
- Flask para a aplicação e Gunicorn para servir o container em produção.
- Textos em `content.json` e URL do Streamlit centralizada em `app.py`.
