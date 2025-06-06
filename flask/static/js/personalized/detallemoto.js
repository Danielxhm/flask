function changeHours(delta) {
  // Si hay fechas seleccionadas, bloquea la selección de horas
  if (document.getElementById('startDate').value || document.getElementById('endDate').value) {
    alert("Has seleccionado fechas. No puedes elegir horas al mismo tiempo.");
    return;
  }

  let input = document.getElementById('hourInput');
  let value = parseInt(input.value) || 0;
  value = Math.max(0, Math.min(24, value + delta)); // límite entre 0 y 24
  input.value = value;
  updatePreview();
}

function updatePreview() {
  let horas = parseInt(document.getElementById('hourInput').value);
  let start = document.getElementById('startDate').value;
  let end = document.getElementById('endDate').value;
  const preview = document.getElementById('preview');
  let mensaje = "";

  // Si hay fechas seleccionadas, resetea horas
  if (start || end) {
    document.getElementById('hourInput').value = 0;
  }

  if (start && end) {
    mensaje = `Reservaste desde <strong>${formatearFecha(start)}</strong> hasta <strong>${formatearFecha(end)}</strong>.`;
  } else if (horas > 0) {
    mensaje = `Has seleccionado <strong>${horas}</strong> hora(s) de alquiler.`;
  } else {
    preview.classList.add("d-none");
    return;
  }

  preview.innerHTML = mensaje;
  preview.classList.remove("d-none");
}

function formatearFecha(fechaISO) {
  const [a, m, d] = fechaISO.split("-");
  return `${d}/${m}/${a}`;
}