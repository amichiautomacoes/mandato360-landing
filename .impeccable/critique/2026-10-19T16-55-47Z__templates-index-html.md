---
target: Landing MANDATO 360
total_score: 23
max_score: 32
na_heuristics: 7,10
p0_count: 0
p1_count: 2
target_identity: "file:D:\\Ativos Tecnologia\\casa_das_maquinas\\Lpaas\\landing\\templates\\index.html"
target_fingerprint: "sha256:90d0cc38d54a6e485a76648e6febcca9cb30e48f0c9ac5aaf03e43becc7c03b8"
target_path: "D:\\Ativos Tecnologia\\casa_das_maquinas\\Lpaas\\landing\\templates\\index.html"
timestamp: 2026-10-19T16-55-47Z
slug: templates-index-html
closed: true
---
Method: dual-agent (A: /root/design_review · B: /root/technical_evidence)

A crítica encontrou uma base sólida, com **23/32 pontos nas heurísticas aplicáveis**. O mapa de Minas Gerais e as capturas reais dão identidade e credibilidade à página. A principal oportunidade está em facilitar o contato e dar mais ritmo à apresentação dos módulos.

| Heurística | Nota | Observação |
|---|---:|---|
| Visibilidade do estado | 3/4 | Galerias e ampliação informam seu estado |
| Linguagem do público | 3/4 | Benefícios claros; há um erro de redação |
| Controle e liberdade | 3/4 | Boa navegação; falta pausa no vídeo |
| Consistência | 3/4 | O mesmo botão verde indica contato e navegação interna |
| Prevenção de erros | 3/4 | Convém explicitar o destino WhatsApp |
| Reconhecimento | 3/4 | Falta uma visão inicial dos quatro módulos |
| Eficiência avançada | n/a | Não é requisito desta landing |
| Estética e concisão | 2/4 | Títulos pesados e blocos muito semelhantes |
| Recuperação de erros | 3/4 | Lightbox oferece mensagem e acesso ao original |
| Documentação | n/a | Não é necessária para decidir pelo contato |
| **Total** | **23/32** | **Bom, com melhorias claras** |

**O que funciona:** especialização territorial evidente, demonstração do produto com imagens reais e bons fundamentos no menu, nas galerias e no lightbox. Nas larguras de 320 a 1440 px verificadas, não houve transbordamento horizontal da página.

**Prioridades:**

1. **P1 — Contato distante no celular.** O hero oferece apenas “Como Funciona”; o WhatsApp fica no menu ou perto do fim da página. Colocar WhatsApp como ação principal da abertura e manter exploração como ação secundária. Comandos: impeccable clarify e layout.
2. **P1 — Movimento sem controle.** O vídeo continua mesmo com movimento reduzido ativado. Adicionar pausa e reprodução, respeitar a preferência e preservar a pausa escolhida. Comandos: impeccable harden e animate.
3. **P2 — Apresentação uniforme dos módulos.** Quatro grandes blocos semelhantes dificultam perceber o conjunto. Acrescentar índice com âncoras e melhorar relação entre nome, benefício e captura. Comandos: impeccable layout e distill.
4. **P2 — Galerias pouco evidentes no desktop.** Navegação depende de descobrir as prévias laterais. Tornar controles, posição e assunto da captura claros. Comandos: impeccable clarify e polish.
5. **P2 — Peso visual excessivo.** Equilibrar pesos da Montserrat, limitar largura dos parágrafos, uniformizar ícones e reduzir sombras e molduras. Corrigir “se influenciou” na introdução. Comandos: impeccable typeset e polish.

**Carga cognitiva e jornada:** carga moderada, com três falhas parciais: movimento disputa atenção, falta visão conjunta dos módulos e sequência longa repete detalhes antes do contato. A abertura estabelece confiança; o centro perde ritmo; o fechamento retoma a proposta, mas não explicita WhatsApp.

**Personas:** Jordan, primeira visita, precisa de clareza sobre o próximo passo. Riley, que avalia o produto, precisa de legendas nas capturas. Casey, no celular, precisa de acesso direto ao contato e posição nas galerias.

**Detector:** dois avisos CLI falsos positivos: broken-image em templates/_lightbox.html:23 (src definido ao abrir) e flat-type-hierarchy em templates/index.html:0 (limitação Jinja). Overlay em navegador: 16 ocorrências, hero-eyebrow-chip ×1, line-length ×1, gpt-thin-border-wide-shadow ×12, overused-font ×1 e kicker-above-heading ×1. O último aviso sobre Montserrat é uma escolha intencional de identidade; priorizar o diagnóstico visual. Overlay executado somente em Chromium headless.

**Observações menores:** conter a placa clara da logo; subordinar a qualificação negativa; adaptar ajuda do lightbox ao toque. Sem P0 identificado. A avaliação não mediu taxa de conversão.

Questions skipped: o usuário já definiu a direção profissional/Persuade e pediu aplicação das melhorias, preservando as informações do produto.
