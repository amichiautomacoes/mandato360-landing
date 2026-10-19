"use strict";

(() => {
  const lightbox = document.querySelector("[data-lightbox]");
  if (!lightbox || typeof lightbox.showModal !== "function") return;

  const area = lightbox.querySelector("[data-lightbox-area]");
  const tela = lightbox.querySelector("[data-lightbox-tela]");
  const imagem = lightbox.querySelector("[data-lightbox-imagem]");
  const titulo = lightbox.querySelector("[data-lightbox-titulo]");
  const status = lightbox.querySelector("[data-lightbox-status]");
  const original = lightbox.querySelector("[data-lightbox-original]");
  const diminuir = lightbox.querySelector("[data-lightbox-diminuir]");
  const aumentar = lightbox.querySelector("[data-lightbox-aumentar]");
  const ajustar = lightbox.querySelector("[data-lightbox-ajustar]");
  const indicador = lightbox.querySelector("[data-lightbox-escala]");
  let origem = null;
  let abertura = 0;
  let pronto = false;
  let escala = 1;
  let larguraBase = 1;
  let alturaBase = 1;
  let gesto = null;

  const atualizarControles = () => {
    diminuir.disabled = !pronto || escala <= 1;
    aumentar.disabled = !pronto || escala >= 8;
    ajustar.disabled = !pronto || escala === 1;
    indicador.value = `${Math.round(escala * 100)}%`;
    area.classList.toggle("lightbox-com-zoom", escala > 1);
  };
  const dimensionar = (x = 0.5, y = 0.5) => {
    const largura = larguraBase * escala;
    const altura = alturaBase * escala;
    const larguraTela = Math.max(area.clientWidth, largura + 32);
    const alturaTela = Math.max(area.clientHeight, altura + 32);
    imagem.style.width = `${largura}px`;
    imagem.style.height = `${altura}px`;
    tela.style.width = `${larguraTela}px`;
    tela.style.height = `${alturaTela}px`;
    area.scrollLeft = (larguraTela - largura) / 2 + largura * x - area.clientWidth / 2;
    area.scrollTop = (alturaTela - altura) / 2 + altura * y - area.clientHeight / 2;
    atualizarControles();
  };
  const ajustarBase = () => {
    if (!pronto) return;
    const proporcao = imagem.naturalWidth / imagem.naturalHeight;
    larguraBase = Math.max(1, Math.min(imagem.naturalWidth, area.clientWidth - 32, (area.clientHeight - 32) * proporcao));
    alturaBase = larguraBase / proporcao;
    dimensionar();
  };
  const ampliar = (novaEscala) => {
    if (!pronto) return;
    // Mantém o detalhe no centro ao aumentar ou reduzir a imagem.
    const x = (area.scrollLeft + area.clientWidth / 2 - (tela.offsetWidth - larguraBase * escala) / 2) / (larguraBase * escala);
    const y = (area.scrollTop + area.clientHeight / 2 - (tela.offsetHeight - alturaBase * escala) / 2) / (alturaBase * escala);
    escala = Math.min(8, Math.max(1, novaEscala));
    dimensionar(escala === 1 ? 0.5 : x, escala === 1 ? 0.5 : y);
  };
  const cancelarArraste = () => {
    gesto = null;
    area.classList.remove("lightbox-arrastando");
  };
  const abrir = async (link) => {
    // A ação da barra aponta para a mesma captura, inclusive durante a transição.
    const galeria = link.closest("[data-carrossel], [data-carrossel-mobile]");
    const origemImagem = link.querySelector("img") ? link : [...(galeria?.querySelectorAll("[data-slide] [data-ampliar]") || [])].find((item) => item.href === link.href);
    const captura = origemImagem?.querySelector("img");
    const slide = captura?.closest("[data-slide]");
    if (!captura) return;
    const versao = ++abertura;
    origem = link;
    pronto = false;
    escala = 1;
    cancelarArraste();
    titulo.textContent = slide?.dataset.title || captura.alt;
    original.href = link.href;
    status.textContent = lightbox.dataset.loading;
    status.hidden = false;
    imagem.hidden = true;
    imagem.alt = captura.alt;
    imagem.src = link.href;
    atualizarControles();
    document.documentElement.classList.add("lightbox-aberto");
    if (!lightbox.open) lightbox.showModal();
    try {
      // O lightbox carrega o PNG original, independentemente do WebP do card.
      await imagem.decode();
      if (versao !== abertura || !lightbox.open) return;
      pronto = true;
      imagem.hidden = false;
      status.hidden = true;
      ajustarBase();
    } catch {
      if (versao !== abertura || !lightbox.open) return;
      status.textContent = lightbox.dataset.error;
    }
  };

  document.addEventListener("click", (evento) => {
    if (evento.defaultPrevented || evento.button !== 0 || evento.ctrlKey || evento.metaKey || evento.shiftKey || evento.altKey) return;
    const link = evento.target.closest("[data-ampliar]");
    if (!link) return;
    evento.preventDefault();
    abrir(link);
  });
  lightbox.querySelector("[data-lightbox-fechar]").addEventListener("click", () => lightbox.close());
  lightbox.addEventListener("click", (evento) => {
    if (evento.target !== lightbox) return;
    const box = lightbox.getBoundingClientRect();
    if (evento.clientX < box.left || evento.clientX > box.right || evento.clientY < box.top || evento.clientY > box.bottom) lightbox.close();
  });
  lightbox.addEventListener("close", () => {
    ++abertura;
    pronto = false;
    cancelarArraste();
    document.documentElement.classList.remove("lightbox-aberto");
    origem?.focus({ preventScroll: true });
    imagem.removeAttribute("src");
    imagem.hidden = true;
  });
  diminuir.addEventListener("click", () => ampliar(escala / 1.5));
  aumentar.addEventListener("click", () => ampliar(escala * 1.5));
  ajustar.addEventListener("click", () => ampliar(1));
  lightbox.addEventListener("keydown", (evento) => {
    if (evento.key === "Tab") {
      const focaveis = [...lightbox.querySelectorAll('button:not(:disabled), a[href], [tabindex="0"]')];
      const primeiro = focaveis[0];
      const ultimo = focaveis[focaveis.length - 1];
      if (evento.shiftKey && (document.activeElement === primeiro || !focaveis.includes(document.activeElement))) {
        evento.preventDefault();
        ultimo?.focus();
      } else if (!evento.shiftKey && (document.activeElement === ultimo || !focaveis.includes(document.activeElement))) {
        evento.preventDefault();
        primeiro?.focus();
      }
    }
    if (evento.ctrlKey || evento.metaKey || evento.altKey) return;
    if (["+", "="].includes(evento.key)) { evento.preventDefault(); ampliar(escala * 1.5); }
    if (evento.key === "-") { evento.preventDefault(); ampliar(escala / 1.5); }
    if (evento.key === "0") { evento.preventDefault(); ampliar(1); }
  });
  // O toque usa a rolagem e o pinch nativos; o mouse pode arrastar a imagem.
  area.addEventListener("pointerdown", (evento) => {
    if (!pronto || escala <= 1 || evento.pointerType !== "mouse" || evento.button !== 0) return;
    evento.preventDefault();
    gesto = { id: evento.pointerId, x: evento.clientX, y: evento.clientY, left: area.scrollLeft, top: area.scrollTop };
    area.setPointerCapture(evento.pointerId);
    area.classList.add("lightbox-arrastando");
  });
  area.addEventListener("pointermove", (evento) => {
    if (!gesto || gesto.id !== evento.pointerId) return;
    area.scrollLeft = gesto.left - (evento.clientX - gesto.x);
    area.scrollTop = gesto.top - (evento.clientY - gesto.y);
  });
  area.addEventListener("pointerup", cancelarArraste);
  area.addEventListener("pointercancel", cancelarArraste);
  area.addEventListener("lostpointercapture", cancelarArraste);
  if ("ResizeObserver" in window) new ResizeObserver(ajustarBase).observe(area);
  else window.addEventListener("resize", ajustarBase);
})();
