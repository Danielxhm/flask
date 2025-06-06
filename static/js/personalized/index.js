
//global comentarios de ms recordatorios de cada error debugueado con gsap para mas interaccion
// GSAP Y SCRIPTS PERSONALIZADOS
document.addEventListener("DOMContentLoaded", function() {
  gsap.registerPlugin(ScrollTrigger);

  // --- SELECTORES GLOBALES ---
  const mainNavbarDesktop = document.getElementById('mainNavbarDesktop');
  const mainNavbarMobile = document.getElementById('mainNavbarMobile'); 
  const heroDesktop = document.getElementById('heroDesktop'); 

  // --- ANIMACIÓN NAVBAR ESCRITORIO ---
  // CSS ya la tiene en: opacity:0, visibility:hidden, transform:translateY(-100%)
  if (mainNavbarDesktop && mainNavbarDesktop.classList.contains('animation1')) {
    gsap.to(mainNavbarDesktop, {
      y: 0, 
      autoAlpha: 1,
      duration: 1, 
      ease: "back.out(1.7)", 
      delay: 0.1
      // NO clearProps: "all" aquí. Quiero que los estilos de GSAP persistan para mantenerla visible.
    });
  }

  // ScrollTrigger para la navbar de escritorio (cambio de fondo)
  if (mainNavbarDesktop && heroDesktop) {
    ScrollTrigger.create({
      trigger: heroDesktop, start: "bottom 60px", 
      onEnter: () => mainNavbarDesktop.classList.add('navbar-scrolled-solid'),
      onLeaveBack: () => mainNavbarDesktop.classList.remove('navbar-scrolled-solid')
    });
  }

  // --- NAVBAR MÓVIL ---
  if (mainNavbarMobile && mainNavbarMobile.classList.contains('animation1-mobile')) {
      // Si .animation1-mobile la oculta inicialmente con CSS (similar a la de escritorio)
      // entonces también necesita un .to() sin clearProps.
      // Ejemplo: #mainNavbarMobile.animation1-mobile { opacity:0; visibility:hidden; }
      const initialOpacity = getComputedStyle(mainNavbarMobile).opacity;
      if (initialOpacity === "0") {
           gsap.to(mainNavbarMobile, { autoAlpha: 1, duration: 0.5, delay: 0.05 }); // Sin clearProps
      }
  }


  // --- MENÚ MÓVIL --- 
  const mobileMenuCollapse = document.getElementById('mobileMenu');
  const togglerMobile = document.querySelector('.navbar-toggler-mobile');
  const topBar = document.querySelector('.navbar-toggler-mobile .top-bar');
  const midBar = document.querySelector('.navbar-toggler-mobile .mid-bar');
  const botBar = document.querySelector('.navbar-toggler-mobile .bot-bar');

  if (mobileMenuCollapse && togglerMobile && topBar && midBar && botBar) {
      function getHamburgerBarOffset() { const barHeight = topBar.offsetHeight || 2; return barHeight + 2; }
      
      const mobileNavItems = mobileMenuCollapse.querySelectorAll('.nav-link');
      // Los nav items están pre-ocultos por CSS

      mobileMenuCollapse.addEventListener('show.bs.collapse', function () {
          document.body.classList.add('modal-open');
          const offset = getHamburgerBarOffset();
          gsap.to(topBar, { rotate: 45, y: offset, duration: 0.3, ease: "power2.inOut" });
          gsap.to(midBar, { opacity: 0, duration: 0.2, ease: "power2.inOut" });
          gsap.to(botBar, { rotate: -45, y: -offset, duration: 0.3, ease: "power2.inOut" });
          
          // El #mobileMenu está pre-oculto por CSS, lo animamo a visible
          gsap.to(mobileMenuCollapse, { autoAlpha: 1, duration: 0.35, ease: 'power2.out' }); // Sin clearProps
          // Los nav-items están pre-ocultos por CSS, los animamo a visibles
          gsap.to(mobileNavItems, { 
              autoAlpha: 1, y: 0, duration: 0.3, stagger: 0.04, ease: 'power2.out', delay: 0.1, clearProps: "all" 
              // clearProps aquí está bien porque el estado final visible se mantiene sin estilos en línea
          });
      });
      mobileMenuCollapse.addEventListener('hide.bs.collapse', function () {
          document.body.classList.remove('modal-open');
          gsap.to(topBar, { rotate: 0, y: 0, duration: 0.3, ease: "power2.inOut" });
          gsap.to(midBar, { opacity: 1, duration: 0.2, delay: 0.1, ease: "power2.inOut" });
          gsap.to(botBar, { rotate: 0, y: 0, duration: 0.3, ease: "power2.inOut" });
          
          gsap.to(mobileMenuCollapse, { autoAlpha: 0, duration: 0.35, ease: 'power2.in', onComplete: () => {
              // Resetear nav items a su estado pre-oculto por CSS para la próxima apertura
              // Esto es importante si el CSS no es suficiente para resetearlos completamente
              gsap.set(mobileNavItems, {
                  opacity:0, 
                  visibility:'hidden', 
                  y: gsap.getProperty(":root", "--gsap-subtle-y-offset")
              });
          }});
      });
      mobileMenuCollapse.querySelectorAll('.nav-link').forEach(link => {
          link.addEventListener('click', () => {
              const bsCollapse = bootstrap.Collapse.getInstance(mobileMenuCollapse);
              if (bsCollapse) { bsCollapse.hide(); }
          });
      });
  }

  // --- HERO SECTIONS ---
  // SIN ANIMACIONES DE ENTRADA GSAP

  // --- ANIMACIONES SUTILES PARA CONTENIDO CON SCROLL ---
  
  function createFadeInUpAnimation(selector, triggerSelector, start = "top 85%", yOffsetVar = "--gsap-subtle-y-offset", staggerAmount = 0.1, duration = 0.7) {
      const elements = document.querySelectorAll(selector);
      if (elements.length > 0) {
          gsap.from(elements, {
              scrollTrigger: {
                  trigger: triggerSelector || elements[0], 
                  start: start,
                  toggleActions: "play none none none",
              },
              autoAlpha: 0,
              y: gsap.getProperty(":root", yOffsetVar) || 15, // Fallback si la variable no está
              duration: duration,
              stagger: elements.length > 1 ? staggerAmount : 0, 
              ease: "power2.out",
              clearProps: "all"
          });
      }
  }

  // Aplicar animaciones sutiles
  const motoPreviewSection = document.getElementById("motos");
  if (motoPreviewSection) {
      createFadeInUpAnimation("#motos h2", "#motos"); 
      createFadeInUpAnimation("#motos p.lead", "#motos", "top 80%"); 
      
      const h2Icon = motoPreviewSection.querySelector("h2 img");
      if (h2Icon) { 
          gsap.to(h2Icon, { 
              scrollTrigger: {
                  trigger: "#motos h2", start: "top 85%", toggleActions: "play none none none",
              },
              rotation: 0, 
              duration: 1.0, ease: "back.out(1.2)", delay: 0.2, 
              clearProps: "transform" 
          });
      }
      createFadeInUpAnimation("#motos .moto-card", "#motos .moto-cards-wrapper", "top 85%", "--gsap-subtle-y-offset", 0.1, 0.6);
  }

  document.querySelectorAll(".btn-effect-3").forEach(btn => {
      if (btn.id !== 'heroDesktopBtn' && btn.id !== 'heroMobileBtn') { 
          gsap.from(btn, {
              scrollTrigger: { trigger: btn, start: "top 85%", toggleActions: "play none none none", once: true },
              autoAlpha: 0, y: 30, scale: 0.95, duration: 0.8, ease: "back.out(1.5)", clearProps: "all"
          });
      }
  });
  
  createFadeInUpAnimation(".testimonials-section h2", ".testimonials-section");
  createFadeInUpAnimation(".testimonial-card", ".testimonials-container", "top 85%", "--gsap-subtle-y-offset", 0.15, 0.6);

  createFadeInUpAnimation(".brands-section .brands-title", ".brands-section");
  createFadeInUpAnimation(".brand-item", ".brands-list", "top 90%", null, 0.05, 0.5); 

  createFadeInUpAnimation(".features-section h2", ".features-section");
  createFadeInUpAnimation(".features-section .col-md-4", ".features-section", "top 75%", "--gsap-subtle-y-offset", 0.15, 0.6);
  
  const featureIcons = document.querySelectorAll(".features-section .feature-icon i");
  if (featureIcons.length > 0) {
      gsap.from(featureIcons, {
          scrollTrigger: { trigger: ".features-section", start: "top 70%", toggleActions: "play none none none"},
          autoAlpha: 0, scale: 0.5, rotation: -45, duration: 0.7, stagger: 0.15, ease: "back.out(1.5)", delay:0.1, clearProps: "all"
      });
  }

  createFadeInUpAnimation(".footer-coolsite-bs .row.gy-4 > .col-lg-4", ".footer-coolsite-bs", "top 90%");
  createFadeInUpAnimation(".footer-coolsite-bs .row.gy-4 > .col-lg-8 .col-lg-6", ".footer-coolsite-bs", "top 90%", "--gsap-subtle-y-offset", 0.1, 0.7);


  const brandsList = document.querySelector(".brands-section .brands-list");
  if(brandsList && brandsList.children.length > 0){ 
      const speed = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--slider-speed').trim()) || 25;
      gsap.to(brandsList, {
          xPercent: -50, duration: speed, repeat: -1, ease: "none"
      });
      const brandsSection = document.querySelector(".brands-section");
      if (brandsSection) {
          brandsSection.addEventListener('mouseenter', () => gsap.to(brandsList, {timeScale: 0.2}));
          brandsSection.addEventListener('mouseleave', () => gsap.to(brandsList, {timeScale: 1}));
      }
  }

}); // Fin de DOMContentLoaded