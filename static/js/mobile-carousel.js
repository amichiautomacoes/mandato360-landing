"use strict";

// A rolagem nativa preserva o deslize, o zoom por gesto e o uso sem JavaScript.
document.querySelectorAll("[data-carrossel-mobile]").forEach((carrossel) => {
  const faixa = carrossel.querySelector("[data-mobile-faixa]");
  const slides = [...faixa.querySelectorAll("[data-slide]")];
  const anterior = carrossel.querySelector("[data-mobile-anterior]");
  const proxima = carrossel.querySelector("[data-mobile-proxima]");
  const status = carrossel.querySelector("[data-mobile-status]");
  const movimentoReduzido = window.matchMedia("(prefers-reduced-motion: reduce)");
  let atual = 0;
  let largura = faixa.clientWidth;
  let anuncio = 0;

  const atualizar = () => {
    if (!faixa.clientWidth || faixa.clientWidth !== largura) return;
    atual = Math.max(0, Math.min(slides.length - 1, Math.round(faixa.scrollLeft / faixa.clientWidth)));
    anterior.disabled = atual === 0;
    proxima.disabled = atual === slides.length - 1;
    slides.forEach((slide, indice) => {
      slide.setAttribute("aria-hidden", String(indice !== atual));
      slide.querySelector("[data-ampliar]").tabIndex = indice === atual ? 0 : -1;
    });
    clearTimeout(anuncio);
    anuncio = setTimeout(() => {
      status.textContent = `${atual + 1} ${carrossel.dataset.of} ${slides.length}: ${slides[atual].dataset.title}`;
    }, 150);
  };
  const navegar = (indice) => {
    const destino = Math.max(0, Math.min(slides.length - 1, indice));
    faixa.scrollTo({ left: destino * faixa.clientWidth, behavior: movimentoReduzido.matches ? "instant" : "smooth" });
  };

  anterior.addEventListener("click", () => navegar(atual - 1));
  proxima.addEventListener("click", () => navegar(atual + 1));
  carrossel.addEventListener("keydown", (evento) => {
    if (evento.altKey || evento.ctrlKey || evento.metaKey) return;
    const destinos = { ArrowLeft: atual - 1, ArrowRight: atual + 1, Home: 0, End: slides.length - 1 };
    if (!(evento.key in destinos)) return;
    evento.preventDefault();
    navegar(destinos[evento.key]);
  });
  faixa.addEventListener("scroll", atualizar, { passive: true });
  // Preserva a imagem selecionada ao girar o celular ou trocar de breakpoint.
  const ajustarTamanho = () => {
    largura = faixa.clientWidth;
    if (!largura) return;
    faixa.scrollTo({ left: atual * largura, behavior: "instant" });
    atualizar();
  };
  if ("ResizeObserver" in window) new ResizeObserver(ajustarTamanho).observe(faixa);
  else window.addEventListener("resize", ajustarTamanho);

  carrossel.querySelector("[data-mobile-controles]").hidden = false;
  carrossel.classList.add("carrossel-mobile-pronto");
  atualizar();
});
