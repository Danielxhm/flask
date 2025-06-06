window.addEventListener('DOMContentLoaded', () => {
  const mainTimeline = gsap.timeline({
      defaults: {
          ease: "power3.out",
          duration: 1
      }
  });

  // Mostrar mensajes flash
  const alerts = document.querySelectorAll('.alert');
  if (alerts.length) {
      gsap.to(alerts, {
          opacity: 1,
          y: 0,
          duration: 0.2,
          stagger: 0.2,
          ease: "back.out(1.2)"
      });
  }

  // Animaciones de entrada respetando diseño actual
  mainTimeline
      .from('.login-right', {
          opacity: 0,
          x: '30%',
          duration: 1.2
      }, 0)

      .from('.login-card', {
          opacity: 0,
          y: 50,
          duration: 1,
          ease: "back.out(1.7)"
      }, 0.3)

      .from('.login-header h2', {
          opacity: 0,
          scale: 0.8,
          duration: 0.8,
          ease: "elastic.out(1, 0.5)"
      }, 0.6)

      .from('.login-header p', {
          opacity: 0,
          y: 20,
          duration: 0.5
      }, 0.8)

      .from('.input-username', {
          opacity: 0,
          x: -30,
          duration: 0.7
      }, 1)

      .from('.input-password', {
          opacity: 0,
          x: -30,
          duration: 0.7
      }, 1.2)

      .from('button[type="submit"]', {
          opacity: 0,
          y: 20,
          duration: 0.8,
          ease: "back.out(2)"
      }, 1.4)

      .from('.register-link', {
          opacity: 0,
          y: 20,
          duration: 0.8
      }, 1.6)

      .from('.textoprm', {
          opacity: 0,
          x: 40,
          duration: 1.2,
          ease: "power2.out"
      }, 1);

  // Efecto hover para botones .boton o .btn
  gsap.utils.toArray('.boton, .btn').forEach(btn => {
      btn.addEventListener('mouseenter', () => {
          gsap.to(btn, {
              scale: 1.05,
              duration: 0.3,
              ease: "power1.out"
          });
      });

      btn.addEventListener('mouseleave', () => {
          gsap.to(btn, {
              scale: 1,
              duration: 0.3,
              ease: "power1.in"
          });
      });
  });

  // Efecto decorativo de fondo suave sin interferir con background-position CSS
  gsap.to('.login-right', {
      backgroundPositionX: '90%',
      duration: 15,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut"
  });
});
