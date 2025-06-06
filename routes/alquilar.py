# routes/alquilar.py
from flask import render_template, flash, session, request, redirect, url_for
from datetime import datetime, timedelta, date
from routes.userdb import obtener_usuarios
from routes.motodb import obtener_motos
from routes.alquileresdb import guardar_alquiler # <--- Ya usa la función modificada

def register_alquilar_routes(app):
    @app.route('/alquilar/<int:id>', methods=['GET', 'POST'])
    def alquilar(id):
        motos = obtener_motos()

        if id not in motos:
            flash('Moto no encontrada.', 'danger')
            return redirect(url_for('dashboard'))

        moto_seleccionada = motos[id]

        if 'username' not in session:
            flash('Debes iniciar sesión para alquilar una moto.', 'warning')
            return redirect(url_for('login', next=url_for('alquilar', id=id)))

        username_actual = session['username']
        usuarios_db = obtener_usuarios()
        email_usuario_actual = None
        if username_actual in usuarios_db and 'email' in usuarios_db[username_actual]:
            email_usuario_actual = usuarios_db[username_actual]['email']
        else:
            print(f"ERROR ALQUILAR: No se pudo encontrar el email para el usuario '{username_actual}'")
            flash('Error al obtener datos del usuario. Intenta iniciar sesión de nuevo.', 'danger')
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            # ... (toda tu lógica de validación de fechas y cálculo de precio sigue igual) ...
            fecha_inicio_str = request.form.get('fecha_inicio')
            fecha_fin_str = request.form.get('fecha_fin')

            if not fecha_inicio_str or not fecha_fin_str:
                flash('Debes seleccionar una fecha de inicio y una fecha de fin.', 'danger')
                return render_template('alquilar.html', moto=moto_seleccionada, id=id)

            # ... (Lógica de conversión de fechas y cálculo de precio) ...
            try:
                fecha_inicio_obj_date = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin_obj_date = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de fecha inválido. Usa YYYY-MM-DD.', 'danger')
                return render_template('alquilar.html', moto=moto_seleccionada, id=id)

            if fecha_fin_obj_date < fecha_inicio_obj_date:
                flash('La fecha de fin no puede ser anterior a la fecha de inicio.', 'danger')
                return render_template('alquilar.html', moto=moto_seleccionada, id=id)

            hoy_date = date.today()
            if fecha_inicio_obj_date < hoy_date:
                flash('No puedes seleccionar una fecha de inicio en el pasado.', 'danger')
                return render_template('alquilar.html', moto=moto_seleccionada, id=id)

            delta = fecha_fin_obj_date - fecha_inicio_obj_date
            duracion_dias = delta.days + 1

            if duracion_dias <= 0:
                 flash('La duración del alquiler debe ser de al menos un día.', 'danger')
                 return render_template('alquilar.html', moto=moto_seleccionada, id=id)

            if 'precio_dia' not in moto_seleccionada or not isinstance(moto_seleccionada['precio_dia'], (int, float)):
                flash('Tarifa diaria de la moto no disponible o inválida. Contacta a soporte.', 'danger')
                return render_template('alquilar.html', moto=moto_seleccionada, id=id)

            precio_total = moto_seleccionada['precio_dia'] * duracion_dias
            unidad_tiempo_str = f"{duracion_dias} día{'s' if duracion_dias != 1 else ''}"
            tipo_tarifa_seleccionada = "dia"

            fecha_inicio_para_guardar_dt = datetime.combine(fecha_inicio_obj_date, datetime.min.time())
            fecha_fin_para_guardar_dt = datetime.combine(fecha_fin_obj_date, datetime.max.time().replace(microsecond=0))


            nuevo_alquiler_data = {
                'username': username_actual,
                'email': email_usuario_actual,
                'moto_id': id,
                'fecha_inicio': fecha_inicio_para_guardar_dt.isoformat(),
                'fecha_fin': fecha_fin_para_guardar_dt.isoformat(),
                'tipo_tarifa': tipo_tarifa_seleccionada,
                'precio_total': precio_total,
                'duracion': unidad_tiempo_str
                # 'estado_aprobacion' se añadirá en guardar_alquiler()
            }
            print(f"Datos para guardar_alquiler (antes de añadir ID y estado): {nuevo_alquiler_data}")

            try:
                guardar_alquiler(nuevo_alquiler_data) # La función se encarga de añadir ID y estado
                flash(f'¡Solicitud de alquiler enviada! Duración: {unidad_tiempo_str}. Precio: ${precio_total:.2f}. Está pendiente de aprobación.', 'info')
                return redirect(url_for('mis_alquileres'))
            except Exception as e:
                print(f"Error al llamar a guardar_alquiler: {e}")
                flash('Ocurrió un error al procesar tu solicitud de alquiler. Por favor, inténtalo de nuevo.', 'danger')
                return redirect(url_for('alquilar', id=id))

        return render_template('alquilar.html', moto=moto_seleccionada, id=id)