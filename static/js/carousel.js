"use strict";

// Coverflow e máscara usam a mesma duração e curva para revelar sem saltos.
document.querySelectorAll("[data-carrossel]").forEach((carrossel) => {
  const palco = carrossel.querySelector(".carrossel-palco");
  const slides = [...carrossel.querySelectorAll("[data-slide]")];
  if (!palco || slides.length < 2 || !Element.prototype.animate) return;

  const status = carrossel.querySelector("[data-carrossel-status]");
  const legenda = carrossel.querySelector("[data-gallery-caption]");
  const descricao = carrossel.querySelector("[data-gallery-description]");
  const movimentoReduzido = window.matchMedia("(prefers-reduced-motion: reduce)");
  const total = slides.length;
  // Com duas capturas, cópias decorativas mantêm a prévia nos dois lados.
  const espelhos = total === 2 ? slides.map((slide) => {
    const espelho = slide.cloneNode(true);
    espelho.removeAttribute("data-slide");
    espelho.removeAttribute("aria-label");
    espelho.removeAttribute("aria-roledescription");
    espelho.setAttribute("aria-hidden", "true");
    espelho.setAttribute("role", "presentation");
    espelho.querySelector("img").alt = "";
    espelho.querySelector("[data-ampliar]").tabIndex = -1;
    palco.append(espelho);
    return espelho;
  }) : [];
  const inteiro = (indice) => (indice + total) % total;
  const relativo = (indice, centro) => {
    const distancia = inteiro(indice - centro);
    return distancia > total / 2 ? distancia - total : distancia;
  };
  const mascara = (lado) => lado > 0
    ? "inset(0% 0% 0% 55%)"
    : lado < 0 ? "inset(0% 55% 0% 0%)" : "inset(0% 0% 0% 0%)";
  const transformar = (x, z, giro, escala) =>
    `translate(-50%, -50%) translate3d(${x}px, 0px, ${z}px) rotateY(${giro}deg) scale(${escala})`;
  const escondido = () => ({ transform: transformar(0, -260, 0, 0.78), opacity: 0 });
  // Galerias maiores mostram apenas a captura central e as duas vizinhas.
  const estado = (lado) => Math.abs(lado) > 1 ? escondido() : ({
    transform: transformar(lado * palco.clientWidth * 0.39, lado ? -100 : 0, lado * -14, lado ? 0.88 : 1),
    opacity: lado ? 0.48 : 1,
  });
  const mascaraEscondida = "inset(0% 42% 0% 42%)";
  let atual = 0;
  let ocupado = false;
  let pendente = null;
  let animacoes = [];
  let gesto = null;
  let ignorarCliqueAte = 0;

  const atualizarInformacao = () => {
    legenda.textContent = slides[atual].dataset.title;
    descricao.textContent = slides[atual].dataset.description || "";
    descricao.hidden = !descricao.textContent;
    status.textContent = `${atual + 1} ${carrossel.dataset.of} ${total}: ${legenda.textContent}${descricao.textContent ? `. ${descricao.textContent}` : ""}`;
  };
  const posicionar = () => {
    slides.forEach((slide, indice) => {
      const lado = relativo(indice, atual);
      Object.assign(slide.style, estado(lado));
      slide.style.zIndex = Math.abs(lado) > 1 ? "0" : lado ? "1" : "3";
      slide.style.pointerEvents = Math.abs(lado) > 1 ? "none" : "auto";
      slide.querySelector(".carrossel-revelacao").style.clipPath = mascara(lado);
      slide.dataset.pos = String(lado);
      slide.setAttribute("aria-hidden", String(lado !== 0));
      slide.querySelector("[data-ampliar]").tabIndex = lado ? -1 : 0;
    });
    espelhos.forEach((espelho, indice) => {
      const oculto = indice === atual;
      Object.assign(espelho.style, oculto ? escondido() : estado(-1));
      espelho.style.zIndex = oculto ? "0" : "1";
      espelho.style.pointerEvents = oculto ? "none" : "auto";
      espelho.querySelector(".carrossel-revelacao").style.clipPath = oculto ? mascaraEscondida : mascara(-1);
      espelho.dataset.pos = oculto ? "oculto" : "-1";
    });
  };

  const navegar = async (destino, direcaoPreferida = 0) => {
    const proximo = inteiro(destino);
    if (ocupado) { pendente = { indice: proximo, direcao: direcaoPreferida }; return; }
    if (proximo === atual) return;
    const anterior = atual;
    atual = proximo;
    ocupado = true;
    carrossel.setAttribute("aria-busy", "true");
    // A próxima captura precisa estar decodificada antes de abrir a máscara.
    await slides[proximo].querySelector("img").decode().catch(() => {});
    const direcao = total === 2 && direcaoPreferida
      ? Math.sign(direcaoPreferida) : Math.sign(relativo(proximo, anterior));
    atualizarInformacao();
    if (!movimentoReduzido.matches) {
      carrossel.classList.add("carrossel-animando");
      const timing = { duration: 700, easing: "cubic-bezier(0.22, 0.75, 0.16, 1)", fill: "both" };
      slides.forEach((slide, indice) => {
        const antes = total === 2 ? (indice === anterior ? 0 : direcao) : relativo(indice, anterior);
        const depois = total === 2 ? (indice === atual ? 0 : -direcao) : relativo(indice, atual);
        const inicio = estado(antes);
        const fim = estado(depois);
        const revelacao = slide.querySelector(".carrossel-revelacao");
        let meio, recorte;
        if (indice === atual) {
          // A lateral cresce, se endireita e abre a máscara de fora para dentro.
          slide.style.zIndex = "4";
          meio = { transform: transformar(direcao * palco.clientWidth * 0.12, -25, direcao * -4, 0.96), opacity: 0.9 };
          recorte = direcao > 0 ? "inset(0% 0% 0% 25%)" : "inset(0% 25% 0% 0%)";
        } else if (indice === anterior) {
          slide.style.zIndex = "3";
          meio = { transform: transformar(-direcao * palco.clientWidth * 0.25, -65, direcao * 10, 0.93), opacity: 0.74 };
          recorte = direcao > 0 ? "inset(0% 28% 0% 0%)" : "inset(0% 0% 0% 28%)";
        } else {
          // As vizinhas entram e saem por trás; as demais continuam ocultas.
          slide.style.zIndex = "0";
          meio = { ...escondido(), opacity: Math.abs(antes) <= 1 || Math.abs(depois) <= 1 ? 0.08 : 0 };
          recorte = "inset(0% 42% 0% 42%)";
        }
        animacoes.push(slide.animate([inicio, { ...meio, offset: 0.48 }, fim], timing));
        animacoes.push(revelacao.animate([
          { clipPath: mascara(antes) }, { clipPath: recorte, offset: 0.48 }, { clipPath: mascara(depois) },
        ], timing));
      });
      espelhos.forEach((espelho, indice) => {
        // Uma prévia recua por trás enquanto a outra reaparece na lateral oposta.
        const saindo = indice === atual;
        const inicio = saindo ? estado(-direcao) : escondido();
        const fim = saindo ? escondido() : estado(direcao);
        espelho.style.zIndex = "1";
        espelho.style.pointerEvents = "none";
        animacoes.push(espelho.animate([
          inicio, { ...escondido(), offset: 0.48 }, fim,
        ], timing));
        animacoes.push(espelho.querySelector(".carrossel-revelacao").animate([
          { clipPath: saindo ? mascara(-direcao) : mascaraEscondida },
          { clipPath: mascaraEscondida, offset: 0.48 },
          { clipPath: saindo ? mascaraEscondida : mascara(direcao) },
        ], timing));
      });
      await Promise.allSettled(animacoes.map((animacao) => animacao.finished));
    }
    posicionar();
    animacoes.forEach((animacao) => animacao.cancel());
    animacoes = [];
    carrossel.classList.remove("carrossel-animando");
    carrossel.removeAttribute("aria-busy");
    ocupado = false;
    if (pendente !== null) {
      const destinoPendente = pendente;
      pendente = null;
      navegar(destinoPendente.indice, destinoPendente.direcao);
    }
  };

  carrossel.classList.add("carrossel-pronto");
  slides.forEach((slide, indice) => {
    slide.querySelector("img").draggable = false;
    slide.querySelector("[data-ampliar]").draggable = false;
    slide.addEventListener("click", (evento) => {
      if (ocupado || indice !== atual) evento.preventDefault();
      if (!ocupado && indice !== atual) navegar(indice);
    });
  });
  espelhos.forEach((espelho, indice) => {
    espelho.querySelector("img").draggable = false;
    espelho.querySelector("[data-ampliar]").draggable = false;
    espelho.addEventListener("click", (evento) => {
      evento.preventDefault();
      if (!ocupado && indice !== atual) navegar(indice, -1);
    });
  });
  posicionar();
  atualizarInformacao();
  const avancar = (passo) => navegar((pendente?.indice ?? atual) + passo, passo);
  carrossel.querySelector("[data-gallery-previous]").addEventListener("click", () => avancar(-1));
  carrossel.querySelector("[data-gallery-next]").addEventListener("click", () => avancar(1));
  carrossel.querySelector("[data-carrossel-controles]").hidden = false;
  carrossel.querySelector("[data-carrossel-legenda]").hidden = false;
  carrossel.addEventListener("keydown", (evento) => {
    const base = pendente?.indice ?? atual;
    const destinos = { ArrowLeft: base - 1, ArrowRight: base + 1, Home: 0, End: total - 1 };
    if (!(evento.key in destinos)) return;
    evento.preventDefault();
    navegar(destinos[evento.key], Math.sign(destinos[evento.key] - base));
  });
  palco.addEventListener("pointerdown", (evento) => {
    if (ocupado || !evento.isPrimary || (evento.pointerType === "mouse" && evento.button !== 0)) return;
    gesto = { id: evento.pointerId, x: evento.clientX, y: evento.clientY, arrastando: false };
  });
  palco.addEventListener("pointermove", (evento) => {
    if (!gesto || gesto.id !== evento.pointerId) return;
    const dx = Math.abs(evento.clientX - gesto.x);
    const dy = Math.abs(evento.clientY - gesto.y);
    if (!gesto.arrastando && dx > 10 && dx > dy * 1.4) {
      gesto.arrastando = true;
      // No toque, a captura implícita já mantém o gesto na imagem.
      if (evento.pointerType !== "touch") palco.setPointerCapture(evento.pointerId);
      carrossel.classList.add("carrossel-arrastando");
    }
  });
  palco.addEventListener("click", (evento) => {
    if (performance.now() < ignorarCliqueAte) { evento.preventDefault(); evento.stopPropagation(); }
  }, true);
  palco.addEventListener("pointerup", (evento) => {
    if (!gesto || gesto.id !== evento.pointerId) return;
    const dx = evento.clientX - gesto.x;
    const dy = evento.clientY - gesto.y;
    if (gesto.arrastando) ignorarCliqueAte = performance.now() + 400;
    gesto = null;
    carrossel.classList.remove("carrossel-arrastando");
    if (Math.abs(dx) >= 35 && Math.abs(dx) > Math.abs(dy) * 1.4) {
      // Evita que o clique sintetizado após o gesto também selecione uma lateral.
      ignorarCliqueAte = performance.now() + 400;
      avancar(dx < 0 ? 1 : -1);
    }
  });
  const cancelarGesto = () => {
    if (gesto?.arrastando) ignorarCliqueAte = performance.now() + 400;
    gesto = null;
    carrossel.classList.remove("carrossel-arrastando");
  };
  palco.addEventListener("pointercancel", cancelarGesto);
  palco.addEventListener("lostpointercapture", (evento) => {
    // Ignora os eventos de perda de captura que sobem dos elementos filhos.
    if (evento.target === palco) cancelarGesto();
  });
  const ajustarTamanho = () => {
    if (ocupado) animacoes.forEach((animacao) => animacao.finish());
    else posicionar();
  };
  if ("ResizeObserver" in window) new ResizeObserver(ajustarTamanho).observe(palco);
  else window.addEventListener("resize", ajustarTamanho);
  movimentoReduzido.addEventListener("change", () => {
    if (movimentoReduzido.matches) animacoes.forEach((animacao) => animacao.finish());
  });
});
