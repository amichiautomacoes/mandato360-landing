---
target: Raio X geral da landing MANDATO 360
total_score: 24
max_score: 32
na_heuristics: 7,10
p0_count: 0
p1_count: 0
target_identity: "file:D:\\Ativos Tecnologia\\casa_das_maquinas\\Lpaas\\landing\\templates\\index.html"
target_fingerprint: "sha256:5942feea2e19a55cc8894883780e7fca370542ec51592b5b512ce0f443e2622c"
target_path: "D:\\Ativos Tecnologia\\casa_das_maquinas\\Lpaas\\landing\\templates\\index.html"
timestamp: 2026-10-19T19-59-24Z
slug: templates-index-html
---
Method: dual-agent (A: /root/design_review · B: /root/technical_evidence)

Raio X da landing MANDATO 360 em 19/10/2026. Alvo: templates/index.html, componentes das galerias e lightbox, CSS, JavaScript, conteúdo e configuração local. Avaliação no modo Persuade; nenhuma alteração na interface.

Atualização de contexto após a avaliação: o responsável confirmou que o objetivo comercial é levar a pessoa a iniciar contato pelo WhatsApp. A recomendação anterior de definir o formato da contratação como prioridade P1 foi revista para uma oportunidade P2 de clareza orientada ao contato. A pontuação abaixo foi mantida como registro da avaliação original; não houve nova bateria de testes nem medição de conversão.

A landing tem identidade própria, boa hierarquia inicial e demonstrações reais da interface. A principal oportunidade comercial é despertar interesse e confiança suficientes para iniciar uma conversa, aproximando o contato do momento de interesse. Há duas correções técnicas para a próxima rodada: ampliação de texto e sequência de foco no lightbox. Não foi demonstrado bloqueio P0 nem falha técnica P1.

## Avaliação de design consolidada

| Heurística | Nota | Evidência |
|---|---:|---|
| Visibilidade do estado | 3/4 | Galerias mostram posição e legenda; lightbox comunica carregamento e erro. |
| Linguagem do público | 3/4 | Tema eleitoral é claro; público e benefício podem ganhar mais destaque antes do contato. |
| Controle e liberdade | 3/4 | Escape, pausa, zoom e retorno de foco funcionam; sequência de Tab do lightbox tem uma lacuna. |
| Consistência e padrões | 3/4 | Identidade coesa; “Como Funciona” abre uma apresentação dos módulos. |
| Prevenção de erros | 3/4 | WhatsApp é sinalizado; capturas podem ser confundidas com controles utilizáveis. |
| Reconhecimento | 3/4 | Índice ajuda; contato desaparece do fluxo durante a leitura móvel. |
| Flexibilidade e eficiência | n/a | Landing sem tarefa operacional recorrente. |
| Estética e concisão | 3/4 | Boa abertura; sequência dos quatro módulos é repetitiva e densa. |
| Recuperação de erros | 3/4 | Erro de imagem oferece mensagem e acesso ao original. |
| Ajuda e documentação | n/a | Documentação operacional não é necessária para decidir pelo contato. |
| **Total** | **24/32 — boa base** | Julgamento heurístico, sem medir conversão. |

A avaliação visual independente A chegou a 25/32. A síntese ajustou Controle e liberdade de 4 para 3 após incorporar a evidência de tabulação de B. A nota não representa porcentagem de acessibilidade nem desempenho comercial.

| Dimensão técnica | Nota | Evidência |
|---|---:|---|
| Acessibilidade | 3/4 | Labels, Escape, pausa e retorno de foco funcionam; ciclo de Tab tem lacuna. |
| Performance | 3/4 | WebP e lazy funcionam; capas duplicadas e oportunidades nos ativos da abertura. |
| Tema e tokens | 3/4 | Identidade consistente; cores literais ainda recorrentes. |
| Responsivo | 2/4 | Cinco larguras padrão funcionam; texto a 200% produz overflow em duas. |
| Integridade da implementação | 3/4 | Componentes coerentes; falhas isoladas, sem defeito sistêmico demonstrado. |
| **Total técnico** | **14/20 — bom** | Auditoria local com correções necessárias. |

O desenho é específico do produto pelos mapas de Minas Gerais e pelas capturas eleitorais, financeiras e políticas. O miolo usa uma composição bastante repetida. A implementação mantém uma identidade coerente; os avisos genéricos de fonte não justificam substituir a Montserrat da marca.

## O que preservar

- Hero com mapa de Minas, promessa legível e contato dourado identificável no desktop e celular.
- Capturas reais, nomes dos módulos acompanhados por perguntas de negócio e navegação independente das galerias.
- Menu móvel, controle do vídeo, movimento reduzido, zoom, Escape e retorno de foco ao fechar a imagem.

Carga cognitiva: baixa, com uma ressalva em oito critérios — manter mentalmente o interesse durante a exploração móvel até reencontrar o contato. Índice e menu apresentam quatro opções. A jornada tem uma abertura forte, uma confirmação pela primeira captura, um vale de repetição nos módulos e um encerramento que pode reforçar o motivo para iniciar uma conversa.

## Prioridades comerciais e de leitura

1. **P2 — Reforçar o valor para iniciar contato.** O objetivo confirmado é levar o visitante ao WhatsApp. “Deputados estaduais” aparece nos metadados, mas não no conteúdo visível; dar destaque a esse público e ao benefício pode ajudar a pessoa a reconhecer a relevância da solução. Avaliar uma chamada que dê um motivo concreto para conversar, usando apenas informações confirmadas. O detalhamento de acesso, auditoria ou contratação é uma informação de apoio, não uma condição para considerar a landing eficaz. Local: content.json:5, content.json:65, content.json:148; templates/index.html:76. Comando: `impeccable clarify`.

2. **P2 — Contextualizar as evidências e estimativas.** As capturas exibem números e classificações sem uma explicação visível de origem, período e natureza dos dados. “Descubra quem são seus eleitores” em content.json:543 é mais definitivo que “composição estimada” em content.json:575. Informar recorte e fontes verificadas, identificar dados demonstrativos quando esse for o caso e qualificar estimativas. A recomendação não pressupõe que os dados estejam incorretos. Comando: `impeccable clarify`.

3. **P2 — Oferecer contato durante a exploração móvel.** Na captura de 390 px, o CTA do hero está em aproximadamente y=357 e o próximo CTA no fluxo em y=6345. O menu continua oferecendo contato, porém fica fechado. Inserir uma chamada contextual discreta entre os módulos, por exemplo após DNA do Eleitor, preservando a leitura e o destino atual. Local: templates/index.html:53 e templates/index.html:153. Comando: `impeccable layout`.

4. **P2 — Reduzir repetição e reforçar o convite no fechamento.** Os módulos ocupam cerca de 3.400 px no desktop e 3.700 px no celular. A qualificação acrescenta benefícios amplos e negativas; o fechamento volta a uma comparação genérica com outras plataformas. Encurtar introduções repetidas e qualificação, preservando fatos. Usar o espaço recuperado para reforçar o benefício e convidar ao contato contextualizado pelo WhatsApp. Local: content.json:1163 e content.json:1187; templates/index.html. Comandos: `impeccable distill` e `impeccable layout`.

5. **P2 — Facilitar a leitura das demonstrações.** A perspectiva e as laterais reduzem o espaço da captura principal no desktop; DNA e DRE exigem inspeção de rótulos pequenos no celular. Dar mais protagonismo à imagem central, manter o Coverflow e tornar “Ampliar captura” explícito. Apresentar uma orientação curta sobre o que observar. Detalhes que já estão recortados dentro do arquivo original precisam ser revistos no próprio asset; o lightbox não os recupera. Local: templates/_carousel.html:11 e templates/_carousel.html:44. Comandos: `impeccable layout` e `impeccable clarify`.

## Achados técnicos confirmados

- **P2 — Reflow com texto ampliado.** A simulação html{font-size:200%} produziu scrollWidth de 363 px em viewport de 320 px e 844 px em 821 px, com compressão da logo e problemas no cabeçalho. O elemento exato causador não foi isolado; candidatos para investigar incluem o índice em duas colunas, o cabeçalho e o breakpoint fixo do menu. Local: static/css/style.css:258 e static/js/main.js:10. Revalidar ampliação real no navegador; o teste realizado foi escala de texto por CSS, não zoom nativo nem certificação WCAG. Comando: `impeccable adapt`.
- **P2 — Ciclo de foco incompleto no lightbox.** O Chromium inclui a área rolável na sequência nativa de Tab, enquanto o código da trap só reconhece botões e links. Ao receber Tab nessa área, o código retorna ao primeiro botão e pula “Abrir original” no avanço. Escape e retorno ao disparador continuam funcionando. Corrigir a lista de elementos focáveis ou aproveitar o comportamento do diálogo nativo, preservando acesso por teclado à imagem e ao link. Local: static/js/lightbox.js:123. Comando: `impeccable harden`.
- **P2 — Download redundante da capa móvel no desktop.** Confirmado carregamento de hero-video-poster-desktop-hq.webp (153.016 bytes) e hero-video-poster-mobile-hq.webp (146.478 bytes). O atributo poster começa com a capa móvel e só é atualizado pelo JavaScript. Evitar esse carregamento desnecessário preservando a capa correta e o fallback. Local: templates/index.html:44 e static/js/main.js. Comando: `impeccable optimize`.
- **P2 — Peso dos ativos da abertura.** Vídeos têm 3.611.992 bytes no desktop e 3.395.969 no celular; logo tem 149.127 bytes. Avaliar uma versão de entrega mais econômica e dimensões adequadas para a logo, preservando os originais e comparando qualidade visual. Tamanho do arquivo não equivale a bytes transferidos em cada visita, especialmente em requisições parciais de vídeo. Comando: `impeccable optimize`.
- **P2 — Candidato intermediário das capturas desktop.** A largura central medida em 1440/DPR1 foi 825 px, mas o navegador escolheu o WebP de 1600 px devido ao salto de 800 para 1600 no srcset. Avaliar um candidato intermediário somente se mantiver a legibilidade dos gráficos e rótulos. Isso é oportunidade de entrega, não evidência de lentidão ou distorção.

## Oportunidades adicionais

- **P2 — Instrumentação de conversão.** Não há analytics ou eventos de clique no código inspecionado. Medir contato por posição (header, hero, chamada intermediária e final) e origem de tráfego para avaliar as hipóteses. Clique no WhatsApp não prova mensagem enviada ou lead qualificado. Instrumentação no proxy ou externa ao repositório não foi verificada.
- **P2 — Apresentação em busca e compartilhamento.** O título atual só identifica a marca; faltam Open Graph e Twitter Cards, imagem de compartilhamento, canonical e favicon. Preparar título descritivo e prévia coerente com o produto, usando o domínio real quando confirmado. A ausência de favicon gerou 404 local. Canonical depende de conhecer o endereço público correto.
- **P3 — Ajuda e acabamento.** Adaptar a ajuda do lightbox para toque, esclarecer a escala “100%” como ajuste à tela, avaliar indicação da seção atual no menu e revisar a faixa clara da primeira captura desktop de DRE.
- **P3 — Arquivos legados e documentação.** static contém 978 arquivos, 81,5 MB; 689 fontes somam 11,1 MB. A interface referencia as duas fontes Montserrat atuais; isso não significa que todas as fontes antigas sejam baixadas. Limpar arquivos comprovadamente sem uso pode reduzir o build. PRODUCT.md e DESIGN.md não existem; documentar produto e decisões visuais ajudaria futuras alterações, sem bloquear a landing atual.

Os riscos variam conforme o visitante: primeira visita pode não reconhecer suficientemente o valor para iniciar uma conversa; quem avalia tecnicamente pode sentir falta da origem e natureza dos dados; quem navega no celular precisa reencontrar contato e ampliar capturas densas. São hipóteses de UX, sem estimar abandono ou ganho de conversão.

## Evidência e limites

Inspeção visual independente em 1440×1000 e 390×844, com navegação dos módulos, imagens e lightbox. Bateria técnica nas larguras 320, 390, 820, 821 e 1440 px em Edge/Chromium headless. Capturas e resultados estão em .impeccable/verification/raiox-current-a* e raiox-current-b*; usar os arquivos *-full-loaded.png para a página completa após carregar imagens lazy.

Detector CLI executado uma vez: dois alertas, ambos falsos positivos após verificar o DOM renderizado: broken-image em templates/_lightbox.html (src é definido ao abrir) e flat-type-hierarchy em templates/index.html (stylesheet com url_for não resolvido pelo detector). O processo retornou código 1 com JSON legível e resolução incompleta do CSS; não foi um scan integral de cores e custom properties. Overlay injetado com sucesso no navegador headless: um alerta genérico sobre Montserrat, escolha deliberada da marca. Não houve overlay visível ao usuário.

Nas cinco larguras padrão não houve overflow. As quatro galerias responderam a Próxima, End e Home, com legendas e contadores atualizados. Menu móvel funcionou por teclado. Lightbox abriu original, ampliou, fechou por Escape e retornou foco; falha deliberada do PNG mostrou mensagem e manteve o link original. Movimento reduzido num contexto novo iniciou sem src e sem requisição de MP4. Pause/play funcionou nas cinco larguras. Nenhuma imagem da variante desktop foi baixada em mobile, nem o inverso. Apenas a Montserrat Latin de 37.956 bytes foi baixada. Não houve pageerror.

Toque sintetizado via CDP avançou a galeria em 320, 390, 821 e 1440; em 820, o gesto de 230 px retornou ao primeiro slide e foi inconclusivo para uma faixa de 754 px. Não foi classificado como defeito. Pares sólidos CSS amostrados tiveram contraste de 9,00:1 no CTA, 11,42:1 no controle do vídeo e 15,02:1 no botão habilitado do lightbox. Não houve medição por pixel dos textos sobre vídeo e gradientes. Sem axe, teste em dispositivo físico, leitor de tela, WebKit/iOS, rede móvel real ou ambiente de produção; sem medição de conversão ou certificação de acessibilidade.

Ordem sugerida: `impeccable adapt` e `impeccable harden` para as duas falhas técnicas; `impeccable clarify` para oferta e dados; `impeccable layout`/`impeccable distill` para contato e ritmo; `impeccable optimize` para carregamento; `impeccable polish` para o acabamento final.
