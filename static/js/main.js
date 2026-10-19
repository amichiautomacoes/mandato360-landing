"use strict";

// Menu mobile: fecha ao navegar, tocar fora, pressionar Escape ou mudar de tela.
(() => {
  const cabecalho = document.querySelector(".cabecalho");
  const botao = document.querySelector(".menu-botao");
  const navegacao = document.getElementById("main-navigation");
  if (!cabecalho || !botao || !navegacao) return;

  const telaPequena = window.matchMedia("(max-width: 820px)");
  const atualizarAltura = () => {
    document.documentElement.style.setProperty("--altura-cabecalho", `${Math.ceil(cabecalho.getBoundingClientRect().height)}px`);
  };
  const definirAberto = (aberto) => {
    botao.setAttribute("aria-expanded", String(aberto));
    botao.setAttribute("aria-label", aberto ? botao.dataset.labelFechar : botao.dataset.labelAbrir);
    navegacao.hidden = telaPequena.matches && !aberto;
  };
  const ajustarTela = () => {
    botao.hidden = !telaPequena.matches;
    definirAberto(false);
    atualizarAltura();
  };

  cabecalho.classList.add("menu-interativo");
  ajustarTela();
  botao.addEventListener("click", () => definirAberto(botao.getAttribute("aria-expanded") !== "true"));
  cabecalho.addEventListener("click", (evento) => {
    if (evento.target.closest("a")) definirAberto(false);
  });
  document.addEventListener("pointerdown", (evento) => {
    if (!cabecalho.contains(evento.target)) definirAberto(false);
  });
  document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape" && botao.getAttribute("aria-expanded") === "true") {
      definirAberto(false);
      botao.focus();
    }
  });
  telaPequena.addEventListener("change", ajustarTela);
  window.addEventListener("resize", atualizarAltura);
  if ("ResizeObserver" in window) new ResizeObserver(atualizarAltura).observe(cabecalho);
})();

// Mantém a navegação nativa das âncoras, preservando foco, hash e histórico.
document.querySelectorAll('a[href^="#"]').forEach((ancora) => {
  ancora.addEventListener("click", () => {
    // Compensa o cabeçalho fixo para manter a seção visível.
    const destino = document.getElementById(ancora.hash.slice(1));
    const alturaCabecalho = document.querySelector(".cabecalho")?.offsetHeight ?? 0;
    if (destino) destino.style.scrollMarginTop = `${alturaCabecalho + 24}px`;

    // Desativa a animação quando o usuário prefere movimento reduzido.
    const movimentoReduzido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    document.documentElement.style.scrollBehavior = movimentoReduzido ? "auto" : "smooth";
  });
});

// O mapa respeita movimento reduzido e a pausa escolhida pelo visitante.
(() => {
  const video = document.getElementById("hero-video");
  const hero = document.querySelector(".hero-com-video");
  const controle = document.querySelector("[data-video-controle]");
  if (!video || !hero || !controle) return;

  const movimentoReduzido = window.matchMedia("(prefers-reduced-motion: reduce)");
  const celular = window.matchMedia("(max-width: 820px)");
  let pausadoPeloUsuario = movimentoReduzido.matches;
  const fonteAtual = () => celular.matches ? video.dataset.srcMobile : video.dataset.srcDesktop;
  const atualizarControle = () => {
    controle.setAttribute("aria-label", video.paused ? controle.dataset.labelReproduzir : controle.dataset.labelPausar);
    controle.querySelector("[data-video-pausa]").hidden = video.paused;
    controle.querySelector("[data-video-reproduzir]").hidden = !video.paused;
  };

  const reproduzir = () => {
    if (document.hidden || pausadoPeloUsuario || video.error) return;
    if (!video.getAttribute("src")) video.src = fonteAtual();
    video.play()?.catch(() => {});
  };

  video.muted = true;
  video.defaultMuted = true;
  video.loop = true;
  video.playsInline = true;
  video.addEventListener("playing", () => {
    hero.classList.add("video-pronto");
    atualizarControle();
  });
  video.addEventListener("pause", atualizarControle);
  video.addEventListener("canplay", reproduzir);
  video.addEventListener("error", () => {
    hero.classList.remove("video-pronto");
    controle.hidden = true;
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) video.pause();
    else reproduzir();
  });
  controle.addEventListener("click", () => {
    pausadoPeloUsuario = !video.paused;
    if (pausadoPeloUsuario) video.pause();
    else reproduzir();
    atualizarControle();
  });
  movimentoReduzido.addEventListener("change", () => {
    pausadoPeloUsuario = movimentoReduzido.matches;
    if (pausadoPeloUsuario) video.pause();
    else reproduzir();
    atualizarControle();
  });
  // A troca de breakpoint mantém a escolha de pausa e atualiza a capa.
  const atualizarFonte = () => {
    hero.classList.remove("video-pronto");
    video.poster = celular.matches ? video.dataset.posterMobile : video.dataset.posterDesktop;
    if (video.getAttribute("src")) video.src = fonteAtual();
    reproduzir();
    atualizarControle();
  };
  celular.addEventListener("change", atualizarFonte);
  controle.hidden = false;
  atualizarFonte();
})();

// Revela as imagens uma única vez, depois de carregarem e entrarem na tela.
(() => {
  const preferenciaMovimento = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (preferenciaMovimento.matches || !("IntersectionObserver" in window)) return;

  const imagens = document.querySelectorAll(".hero-imagem, .modulo-imagem");
  const observador = new IntersectionObserver((entradas) => {
    entradas.forEach((entrada) => {
      if (!entrada.isIntersecting) return;
      observador.unobserve(entrada.target);

      const imagem = entrada.target.querySelector("img");
      const revelar = () => entrada.target.classList.add("imagem-visivel");
      if (!imagem || imagem.complete) {
        revelar();
      } else {
        imagem.addEventListener("load", revelar, { once: true });
        imagem.addEventListener("error", revelar, { once: true });
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -24px 0px" });

  // Sem JavaScript ou suporte ao observador, as imagens continuam visíveis.
  imagens.forEach((imagem) => {
    imagem.classList.add("imagem-entrada");
    observador.observe(imagem);
  });

  preferenciaMovimento.addEventListener("change", (evento) => {
    if (!evento.matches) return;
    observador.disconnect();
    imagens.forEach((imagem) => imagem.classList.add("imagem-visivel"));
  });
})();
