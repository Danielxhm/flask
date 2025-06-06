  // Variables de Jinja2
  const precioHora = parseFloat("{{ moto.precio_hora | default(0) }}"); 
  const precioDia = parseFloat("{{ moto.precio_dia | default(0) }}");
  const motoId = parseInt("{{ id | default(0) }}");


  // Selectores del DOM
  const startDateInput = document.getElementById("startDate");
  const endDateInput = document.getElementById("endDate");
  const preview = document.getElementById("preview");
  const previewDetails = document.getElementById("previewDetails");
  const totalAmountDisplay = document.getElementById("totalAmount");
  const dateSelectionContainer = document.getElementById("dateSelectionContainer"); // Contenedor de los inputs de fecha

  document.addEventListener("DOMContentLoaded", () => {
      // Ocultar selectores de fecha si el usuario no está logueado
      // Esto ya se maneja con el bloque Jinja if 'username' in session que envuelve el dateSelectionContainer
      // por lo que el siguiente bloque JS es redundante si el HTML está estructurado así.
      // if (!isUserLoggedIn && dateSelectionContainer) {
      //     dateSelectionContainer.style.display = 'none';
      // }

      if (isUserLoggedIn && startDateInput && endDateInput) {
          const now = new Date();
          const todayISO = getISODate(now);

          startDateInput.min = todayISO;
          endDateInput.min = todayISO; 

          startDateInput.addEventListener("change", handleDateChange);
          endDateInput.addEventListener("change", handleDateChange);
          
          updatePreview(); // Llamar para actualizar el preview si hay valores iniciales (ej. al volver a la pág.)
      }
  });

  function getISODate(dateObj) {
      if (!dateObj || !(dateObj instanceof Date) || isNaN(dateObj.getTime())) return "";
      const offset = dateObj.getTimezoneOffset();
      const localDate = new Date(dateObj.getTime() - (offset * 60 * 1000));
      return localDate.toISOString().split('T')[0];
  }

  function parseDateAsUTC(dateStr) {
      if (!dateStr) return null;
      const parts = dateStr.split('-');
      if (parts.length !== 3) return null;
      const [year, month, day] = parts.map(Number);
      if (isNaN(year) || isNaN(month) || isNaN(day)) return null;
      try {
          return new Date(Date.UTC(year, month - 1, day));
      } catch (e) {
          console.error("Error al parsear fecha:", dateStr, e);
          return null;
      }
  }

  function handleDateChange() {
      if (!startDateInput || !endDateInput) return;

      const todayISO = getISODate(new Date());

      if (startDateInput.value && startDateInput.value < todayISO) {
          startDateInput.value = todayISO; 
      }

      if (startDateInput.value) {
          endDateInput.min = startDateInput.value; 
          if (endDateInput.value && endDateInput.value < startDateInput.value) {
              endDateInput.value = startDateInput.value; // Forzar a que fin no sea antes que inicio
          }
      } else {
          endDateInput.min = todayISO;
      }
      updatePreview();
  }

  function updatePreview() {
      if (!isUserLoggedIn) { // Si no está logueado, no hacer nada con el preview
          if (preview) preview.classList.add("d-none");
          if (totalAmountDisplay) totalAmountDisplay.innerText = "$0.00";
          if (previewDetails) previewDetails.innerHTML = "";
          return;
      }
      // Asegurar que los elementos del DOM existen antes de usarlos
      if (!preview || !previewDetails || !totalAmountDisplay || !startDateInput || !endDateInput) {
          console.warn("Faltan elementos del DOM para el preview del alquiler.");
          return;
      }


      const startDateVal = startDateInput.value;
      const endDateVal = endDateInput.value;

      let totalEstimatedCost = 0;
      let durationDetails = "";
      let displayPreview = false;
      
      if (startDateVal && endDateVal) {
          const startDateTime = parseDateAsUTC(startDateVal); 
          const endDateTime = parseDateAsUTC(endDateVal);     

          if (startDateTime && endDateTime && endDateTime.getTime() >= startDateTime.getTime()) {
              const diffMilliseconds = endDateTime.getTime() - startDateTime.getTime();
              // Política: Días inclusivos. 
              // (ej. 30/05 a 31/05 son 2 días, 30/05 a 30/05 es 1 día)
              let calculatedDays = Math.floor(diffMilliseconds / (1000 * 60 * 60 * 24)) + 1;

              if (calculatedDays <= 0) calculatedDays = 1; 

              if (precioDia > 0) {
                  totalEstimatedCost = calculatedDays * precioDia;
                  durationDetails = `<li>${calculatedDays} día(s) × $${precioDia.toFixed(2)}/día = <strong>$${totalEstimatedCost.toFixed(2)}</strong></li>`;
                  displayPreview = true;
              } else {
                  durationDetails = `<li>${calculatedDays} día(s) seleccionados (tarifa por día no disponible)</li>`;
                  displayPreview = true; 
              }
          }
      }

      if (displayPreview) {
          preview.classList.remove("d-none");
          previewDetails.innerHTML = durationDetails;
          totalAmountDisplay.innerText = `$${totalEstimatedCost.toFixed(2)}`;
      } else {
          preview.classList.add("d-none");
          previewDetails.innerHTML = "";
          totalAmountDisplay.innerText = "$0.00";
      }
  }

  function changeMainImage(newSrc) {
      const mainImage = document.getElementById('mainImage');
      if (mainImage) {
          mainImage.src = newSrc;
          const thumbnails = document.querySelectorAll('.product-gallery .img-thumbnail');
          if (thumbnails) {
              thumbnails.forEach(thumb => {
                  thumb.classList.remove('active-thumbnail');
                  if (thumb.src === newSrc) {
                      thumb.classList.add('active-thumbnail');
                  }
              });
          }
      }
  }