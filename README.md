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
As imagens aparecem com uma transição suave de opacidade e deslocamento ao
entrarem na tela, uma vez por imagem e após o carregamento. A animação usa
`IntersectionObserver` e respeita a preferência por movimento reduzido;
sem JavaScript ou suporte ao observador, as imagens ficam visíveis normalmente.

As imagens dos módulos usam `picture` com versões WebP de 480, 800 e 1200 px em
`static/img/responsive/`, mantendo os PNGs como fallback. Os campos `width` e
`height` reservam o espaço das imagens; `sources` define as versões responsivas.
As imagens dos módulos usam lazy loading. Na revisão em 360 px com densidade 2×,
as quatro versões selecionadas somaram aproximadamente 254 KB. Esse valor é o
peso dos arquivos, não uma medição de tempo em uma rede real.

Para regenerar os WebP após trocar uma imagem, atualize seus caminhos e dimensões
no JSON e execute na pasta `Lpaas`, com a venv que já contém Playwright:

```powershell
.\.venv\Scripts\python.exe landing\tools\optimize_images.py
```

O hero usa a animação de `../assets/download.mp4`, com aproximadamente dez
segundos e proporção vertical 9:16. O vídeo cobre todo o fundo da primeira seção
no celular e no desktop, usando `object-fit: cover`, com enquadramento adaptado
e luminosidade original, com textos e botões em primeiro plano. A seção
ocupa pelo menos a altura disponível da tela abaixo do cabeçalho. O vídeo
inicia automaticamente, sem som, em loop, e
continua ao rolar a página, sem controles de reprodução visíveis. Ao trocar
de aba, a reprodução pausa e retoma automaticamente no retorno.

`hero.video` no JSON centraliza os arquivos, as dimensões e a capa.
As versões em `static/video/` usam H.264: 540 × 960 px e cerca de 450 KB para
celular, 720 × 1280 px e cerca de 744 KB para desktop. A capa WebP mantém o
visual durante o carregamento, em caso de falha ou sem JavaScript. O vídeo
original é preservado. Para regenerar os arquivos e as capas:

```powershell
.\.venv\Scripts\python.exe landing\tools\prepare_hero_video.py
```

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
das ações e blur de 12 px no cabeçalho e 20 px com saturação de 1,4 nos cards.
As variáveis de `:root`, como `--cor-primaria`, `--fonte-corpo`,
`--fonte-titulo`, `--espaco-6` e `--blur-vidro`, permitem ajustar a identidade.

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
Grid e Flexbox controlam o layout; os cards têm fundo opaco como fallback quando
o navegador não suporta `backdrop-filter`.

As quatro imagens dos módulos são ilustrativas, como as referências da página
extraída; não são capturas do dashboard real. Para usar prints reais, copie os
arquivos para `static/img/` e altere `solution.modules[].image.path`, os respectivos
textos `alt`, dimensões, `sources` e `solution.image_note` no JSON. Gere novamente
as versões WebP com o comando acima. O caminho de cada imagem é relativo à pasta
`static/`, por exemplo `img/raiox.png`.

## Boas práticas

- Código comentado em português e classes CSS com nomes em português.
- Imagens, SVGs, fontes, CSS e JavaScript locais, sem CDNs externas.
- JavaScript puro para menu mobile, rolagem de âncoras e entrada das imagens.
- Flask para a aplicação e Gunicorn para servir o container em produção.
- Textos em `content.json` e URL do Streamlit centralizada em `app.py`.
