document.addEventListener("DOMContentLoaded", function () {
  const flashContainer = document.getElementById("flash-container");

  flashContainer?.addEventListener("closed.bs.alert", () => {
    const remainingAlerts = flashContainer.querySelectorAll(".alert.show");
    if (remainingAlerts.length === 0) {
      // Alternativa 1: oculta completamente
      // flashContainer.classList.add("hidden");

      // Alternativa 2: solo reduce margen (más elegante)
      flashContainer.classList.add("reduced-margin");
    }
  });
});
