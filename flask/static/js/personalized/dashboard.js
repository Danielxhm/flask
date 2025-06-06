document.addEventListener('DOMContentLoaded', function () {
  // Inicializar GSAP y ScrollTrigger
  gsap.registerPlugin(ScrollTrigger);

  // Animación del navbar
  const navbar = document.querySelector('.navbar');
  const heroSection = document.querySelector('#hero-section');
  let lastScrollTop = 0;

  // Función para detectar si el navbar está sobre el hero section
  function isNavbarOverHero() {
      if (!heroSection) return false;

      const heroBottom = heroSection.offsetTop + heroSection.offsetHeight;
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

      return scrollTop < (heroBottom - navbar.offsetHeight);
  }

  // Comprobación inicial del navbar
  if (isNavbarOverHero()) {
      navbar.classList.add('at-hero');
  }

  // Control del scroll para el navbar
  window.addEventListener('scroll', function () {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

      // Verificar si el navbar está sobre el hero
      if (isNavbarOverHero()) {
          navbar.classList.add('at-hero');
      } else {
          navbar.classList.remove('at-hero');
      }

      // Ocultar/mostrar navbar al hacer scroll
      if (scrollTop > lastScrollTop && scrollTop > 100) {
          navbar.classList.add('hidden');
      } else {
          navbar.classList.remove('hidden');
      }

      lastScrollTop = scrollTop;
  });

  // Animación del header con GSAP
  gsap.to("#colorheader", {
      opacity: 1,
      y: 0,
      duration: 1,
      ease: "power3.out",
      delay: 0.2
  });

  // Animación para las tarjetas de perfil
  gsap.to(".profile-card", {
      opacity: 1,
      y: 0,
      duration: 0.8,
      ease: "power3.out",
      scrollTrigger: {
          trigger: ".profile-card",
          start: "top 90%"
      }
  });

  // Animación para la tarjeta de instrucciones
  gsap.to(".instructions-card", {
      opacity: 1,
      y: 0,
      duration: 0.8,
      ease: "power3.out",
      delay: 0.2,
      scrollTrigger: {
          trigger: ".instructions-card",
          start: "top 90%"
      }
  });

  // Animación para los títulos de sección
  gsap.utils.toArray('.animate-fade-up').forEach(element => {
      gsap.to(element, {
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: "power3.out",
          scrollTrigger: {
              trigger: element,
              start: "top 85%"
          }
      });
  });

  // Animación para las tarjetas de motos (efecto escalonado)
  const bikeCards = document.querySelectorAll('.bike-card');
  bikeCards.forEach((card, index) => {
      gsap.to(card, {
          opacity: 1,
          y: 0,
          duration: 0.6,
          ease: "power3.out",
          delay: 0.1 * index, // Efecto escalonado
          scrollTrigger: {
              trigger: card,
              start: "top 85%"
          }
      });
  });
});