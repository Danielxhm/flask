# routes/adminpanel.py
from flask import render_template, flash, session, request, redirect, url_for, jsonify
from routes.userdb import obtener_usuarios, eliminar_usuario
from routes.alquileresdb import obtener_todos_los_alquileres, actualizar_estado_aprobacion_alquiler, obtener_alquiler_por_id
from routes.motodb import obtener_motos, actualizar_stock, obtener_moto_por_id
from datetime import datetime

def abreviar(numero):
    try:
        numero = float(numero)
        if numero >= 1_000_000_000:
            return f'{numero/1_000_000_000:.1f}B'
        elif numero >= 1_000_000:
            return f'{numero/1_000_000:.1f}M'
        elif numero >= 1_000:
            return f'{numero/1_000:.1f}K'
        else:
            return f'{numero:.0f}'
    except (ValueError, TypeError):
        return 0


def register_admin_routes(app):
    @app.route('/admin')
    def admin():
        if session.get('username') != 'admin':
         flash('Acceso no autorizado.', 'danger')
         return redirect(url_for('login'))

        usuarios = obtener_usuarios()
        usuario_key = session['username']
        if usuario_key not in usuarios:
            session.clear()
            flash('Tu sesión ha expirado. Por favor inicia sesión nuevamente.', 'warning')
            return redirect(url_for('login'))


        usuarios_dict = obtener_usuarios()

        print(f"DEBUG: Usuarios obtenidos => {usuarios_dict}")
        todos_los_alquileres = obtener_todos_los_alquileres()
        motos_dict = obtener_motos()


        # --- Datos para el Resumen General (Clientes, Reservas, Ingresos) ---
        cantidad_total_clientes = len(usuarios_dict)
        cantidad_total_reservas_aprobadas = 0
        ingresos_totales_aprobados = 0

        for alq in todos_los_alquileres:
            if alq.get('estado_aprobacion') == 'aprobado':
                cantidad_total_reservas_aprobadas += 1
                try:
                    ingresos_totales_aprobados += float(alq.get('precio_total', 0))
                except (ValueError, TypeError):
                    print(f"ADVERTENCIA ADMIN: No se pudo convertir precio_total a float para el alquiler ID {alq.get('id_alquiler')}")

        print(f"DEBUG ADMIN: Clientes: {cantidad_total_clientes}, Reservas Aprobadas: {cantidad_total_reservas_aprobadas}, Ingresos: {ingresos_totales_aprobados}")


        # --- 1. Solicitudes de Alquiler Pendientes ---
        solicitudes_pendientes = []
        for alq in todos_los_alquileres:
            if alq.get('estado_aprobacion') == 'pendiente':
                usuario_info = usuarios_dict.get(alq.get('username'))
                moto_info = motos_dict.get(alq.get('moto_id'))
                if usuario_info and moto_info:
                    solicitudes_pendientes.append({
                        'id_alquiler': alq.get('id_alquiler'),
                        'nombre_usuario': usuario_info.get('nombre', alq.get('username')),
                        'email_usuario': usuario_info.get('email', 'N/A'),
                        'nombre_moto': moto_info.get('nombre', 'Moto Desconocida'),
                        'precio_moto_dia': moto_info.get('precio_dia', 0),
                        'precio_total_solicitud': alq.get('precio_total', 0),
                        'fecha_inicio': alq.get('fecha_inicio'), # Se pasa como string ISO
                        'fecha_fin': alq.get('fecha_fin'),       # Se pasa como string ISO
                        'duracion': alq.get('duracion')
                    })
        print(f"DEBUG ADMIN: Solicitudes pendientes: {solicitudes_pendientes}")


        # --- 2. Tabla de Resumen de Usuarios y sus Reservas ---
        resumen_usuarios = []
        for username, datos_usuario in usuarios_dict.items():
            email = datos_usuario.get('email', 'N/A')
            nombre = datos_usuario.get('nombre', username)
            reservas_aprobadas = 0
            reservas_rechazadas = 0
            reservas_pendientes_usuario = 0
            for alq_resumen in todos_los_alquileres: # Usar variable diferente para no confundir
                # Asumiendo que la identificación principal del alquiler con el usuario es por 'email'
                if alq_resumen.get('email') == email:
                    if alq_resumen.get('estado_aprobacion') == 'aprobado':
                        reservas_aprobadas += 1
                    elif alq_resumen.get('estado_aprobacion') == 'rechazado':
                        reservas_rechazadas += 1
                    elif alq_resumen.get('estado_aprobacion') == 'pendiente':
                        reservas_pendientes_usuario +=1

            estado_general_usuario = "Inactivo"
            # Un usuario es activo si tiene reservas aprobadas o pendientes
            if reservas_aprobadas > 0 or reservas_pendientes_usuario > 0:
                estado_general_usuario = "Activo"

            resumen_usuarios.append({
                'nombre': nombre,
                'email': email,
                'estado_general': estado_general_usuario,
                'aprobadas': reservas_aprobadas,
                'rechazadas': reservas_rechazadas,
                'pendientes': reservas_pendientes_usuario
            })
        print(f"DEBUG ADMIN: Resumen de usuarios: {resumen_usuarios}")

        # --- 3. Tabla de Administración de Usuarios (la que ya tenías) ---
        usuarios_para_admin_tabla = [] # Renombrado para evitar conflicto de nombres
        for username, datos_usuario in usuarios_dict.items():
            email_u = datos_usuario.get('email', '')
            nombre_u = datos_usuario.get('nombre', username)
            # Contar solo aprobadas para la columna "reservas" de esta tabla
            num_reservas_aprob_u = sum(1 for a in todos_los_alquileres if a.get('email') == email_u and a.get('estado_aprobacion') == 'aprobado')
            usuarios_para_admin_tabla.append({
                'username': username,
                'nombre': nombre_u,
                'email': email_u if email_u else "No especificado",
                'reservas': num_reservas_aprob_u # Número de reservas aprobadas para este usuario
            })

        cantidad_motos_total_sistema = len(motos_dict) # Renombrado para claridad

        return render_template(
            'dashboardadmin.html',
            # Datos para el resumen general
            total_clientes=cantidad_total_clientes,
            total_reservas=cantidad_total_reservas_aprobadas,
            ingresos_totales=ingresos_totales_aprobados,
            motos=motos_dict,
            # Datos para las tablas específicas
            solicitudes_pendientes=solicitudes_pendientes,
            resumen_usuarios=resumen_usuarios,
            usuarios_para_admin=usuarios_para_admin_tabla, # Usar el nombre renombrado
            cantidad_motos=cantidad_motos_total_sistema, # Usar el nombre renombrado
            datetime=datetime, # Pasar el módulo datetime para usarlo en la plantilla
            usuario=usuarios[usuario_key]
        )

    @app.route('/admin/procesar_solicitud/<id_alquiler>/<accion>', methods=['POST'])
    def procesar_solicitud_admin(id_alquiler, accion):
        if session.get('username') != 'admin':
            flash('Acceso no autorizado.', 'danger')
            return redirect(url_for('login'))

        if accion not in ['aprobar', 'rechazar']:
            flash('Acción no válida.', 'danger')
            return redirect(url_for('admin'))

        if accion == 'rechazar':
            # Rechazo no requiere verificación de stock
            exito_estado = actualizar_estado_aprobacion_alquiler(id_alquiler, 'rechazado')
            flash('Solicitud rechazada.', 'info' if exito_estado else 'danger')
            return redirect(url_for('admin'))

        # Aquí llega solo si la acción es aprobar
        alquiler = obtener_alquiler_por_id(id_alquiler)
        if not alquiler:
            flash('Alquiler no encontrado.', 'danger')
            return redirect(url_for('admin'))

        moto_id = alquiler.get('moto_id')
        if not moto_id:
            flash('ID de moto no disponible.', 'danger')
            return redirect(url_for('admin'))

        # Verificar stock antes de aprobar
        moto = obtener_moto_por_id(moto_id)
        if not moto or moto.get('stock', 0) <= 0:
            flash('No hay stock suficiente para esa moto. No se puede aprobar.', 'warning')
            return redirect(url_for('admin'))

        # Actualizar estado del alquiler a aprobado
        exito_estado = actualizar_estado_aprobacion_alquiler(id_alquiler, 'aprobado')
        if not exito_estado:
            flash('No se pudo actualizar el estado del alquiler.', 'danger')
            return redirect(url_for('admin'))

        # Disminuir stock
        exito_stock = actualizar_stock(moto_id, -1)
        if not exito_stock:
            # ⚠️ Esto no debería ocurrir si validaste antes, pero por seguridad:
            flash('Error al actualizar el stock después de aprobar.', 'danger')
            # Opcional: revertir estado del alquiler
            actualizar_estado_aprobacion_alquiler(id_alquiler, 'pendiente')

        flash(f'Solicitud {id_alquiler} marcada como "aprobado".', 'success')
        return redirect(url_for('admin'))



    @app.route('/admin/delete_user/<username_a_eliminar>', methods=['POST'])
    def delete_user_route(username_a_eliminar):
        success, message = eliminar_usuario(username_a_eliminar)
        if success:
            flash(message, 'success')
        else:
            flash(message, 'danger')
        return redirect(url_for('admin'))
