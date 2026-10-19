---
version: 1
slug: "templates-index-html"
primary_target: "templates/index.html"
related_targets: ["static/css/style.css","static/js/main.js","templates/_carousel.html"]
---

# Landing MANDATO 360

Mode: Persuade

Target: templates/index.html

Refinamento da landing existente, solicitado em 19/10/2026 após critique. O visitante precisa entender a proposta, reconhecer os quatro módulos, examinar as capturas reais e iniciar contato pelo WhatsApp.

Objetivo comercial confirmado pelo responsável: levar a pessoa interessada a iniciar contato pelo WhatsApp. Avaliar conteúdo, hierarquia e navegação pela capacidade de despertar interesse, construir confiança e facilitar essa conversa. O detalhamento da contratação é uma informação de apoio, cuja necessidade deve ser justificada pelo efeito sobre o contato; não é um requisito de compra dentro da landing. Cliques no WhatsApp são um indicador de intenção, distinto de conversa iniciada.

Preservar Montserrat, azul-marinho, dourado, logo, mapas e vídeos de Minas Gerais, capturas desktop/mobile, conteúdo factual e destino do contato. Sem novos números, depoimentos, promessas ou credenciais.

Logo atualizada a pedido do responsável: usar a versão branca e transparente de `../assets/Logo Branca.png` no header e no rodapé, sem base clara ou alteração do arquivo original. Preservar a proporção e a leitura no desktop e no celular.

Direção: tipografia mais leve e hierarquia clara; dourado da marca identifica contato, ação secundária conduz aos módulos; índice de quatro âncoras; nomes de módulos em destaque e ícones SVG consistentes; molduras discretas e maior protagonismo das capturas. Controle do vídeo e preferência por movimento reduzido. Galerias mantêm Coverflow, swipe, teclado e lightbox, com contexto visível.

Contato persistente solicitado pelo responsável: botão circular de WhatsApp verde no canto inferior esquerdo, fixo durante a rolagem no desktop e celular. Usar o destino existente do JSON, ícone SVG local, alvo de 56 px, recuo com área segura e foco visível. Ocultar durante o lightbox e reservar espaço no fim do rodapé.

Leitura dos módulos: resumos diretos e distintos, preservando nomes, perguntas e informações factuais. A barra antes de cada captura apresenta assunto, posição e ação visível “Ampliar captura”; a explicação fica abaixo. A captura central desktop ocupa 84% do palco mantendo Coverflow e proporção. A ação acompanha a imagem selecionada e devolve foco ao fechar o lightbox. No celular, a ajuda usa instruções de toque e botões de zoom.

Fechamento solicitado com referência visual: título “Sua próxima decisão política merece mais do que intuição.”, apresentação integrada dos dados, três benefícios (proteger a base, encontrar oportunidades, decidir com dados) e ação “Solicitar uma apresentação personalizada”, com destino ao WhatsApp existente. Adaptar à Montserrat, azul e dourado; três blocos paralelos no desktop e uma coluna compacta no celular. O título lidera a hierarquia; “Inteligência para decisões estratégicas” identifica semanticamente a lista de benefícios, sem um rótulo decorativo acima do título.

Restrição explícita de mídia: otimizar carregamento sem perder qualidade dos vídeos ou imagens. Preservar resolução, FPS, cores e todos os quadros; sem aumentar CRF ou recomprimir imagens. A capa fica exclusivamente no picture responsivo, evitando o poster mobile duplicado pelo video no desktop. Os WebP, PNGs originais, srcset e lazy loading permanecem. Qualquer redução do MP4 exige cópia de faixa e prova de quadros/tempos idênticos; se a economia for pequena, registrar o resultado sem prometer compressão maior.

Verificar desktop, celular, larguras ao redor de 820 px, zoom, teclado, contraste, pausa do vídeo e degradação sem JavaScript. Sem decisões pendentes para este escopo.
