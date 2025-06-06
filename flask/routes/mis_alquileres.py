# routes/mis_alquileres.py
from flask import render_template, session, redirect, url_for, flash
from routes.alquileresdb import obtener_todos_los_alquileres
from routes.motodb import obtener_motos
from routes.userdb import obtener_usuarios # Necesitas esto para obtener el email
from datetime import datetime

def register_mis_alquileres_routes(app):
    @app.route('/mis_alquileres')
    def mis_alquileres():
        if 'username' not in session:
            flash('Debes iniciar sesión para ver tus alquileres.', 'warning')
            return redirect(url_for('login', next=url_for('mis_alquileres')))

        username_actual = session['username']

        # --- OBTENER EMAIL DEL USUARIO ACTUAL ---
        usuarios_db = obtener_usuarios()
        email_usuario_actual = None
        if username_actual in usuarios_db and 'email' in usuarios_db[username_actual]:
            email_usuario_actual = usuarios_db[username_actual]['email']
        else:
            print(f"ERROR MIS_ALQUILERES: No se pudo encontrar el email para el usuario '{username_actual}'")
            flash('Error al obtener datos del usuario. Intenta iniciar sesión de nuevo.', 'danger')
            return redirect(url_for('dashboard'))

        if not email_usuario_actual: # Seguridad adicional
            flash('No se pudo verificar tu email para mostrar los alquileres.', 'danger')
            return redirect(url_for('dashboard'))

        todos_los_alquileres = obtener_todos_los_alquileres()
        print(f"DEBUG MIS_ALQUILERES: Todos los alquileres obtenidos: {todos_los_alquileres}")
        print(f"DEBUG MIS_ALQUILERES: Buscando alquileres para email: {email_usuario_actual}")

        mis_alquileres_filtrados = []
        for alq in todos_los_alquileres:
            print(f"DEBUG MIS_ALQUILERES: Procesando alquiler: {alq}")
            # Filtra por el email del usuario
            if alq.get('email') == email_usuario_actual: # <--- CAMBIO CLAVE AQUÍ
                # Crear una copia del diccionario del alquiler para no modificar la lista original
                # si se va a usar en otros lugares, y para asegurar que cada usuario tenga su propia
                # instancia de objeto fecha si es necesario.
                alquiler_copia = dict(alq)

                # Convertir fechas de string a datetime si es necesario en la copia
                if isinstance(alquiler_copia.get('fecha_inicio'), str):
                    try:
                        alquiler_copia['fecha_inicio'] = datetime.fromisoformat(alquiler_copia['fecha_inicio'])
                    except ValueError:
                        print(f"ADVERTENCIA MIS_ALQUILERES: Formato de fecha_inicio inválido en alquiler: {alquiler_copia}")
                        continue # Saltar este alquiler si la fecha es inválida
                elif not isinstance(alquiler_copia.get('fecha_inicio'), datetime):
                    # Si no es string ni datetime, es un problema.
                    print(f"ADVERTENCIA MIS_ALQUILERES: Tipo de fecha_inicio inesperado: {type(alquiler_copia.get('fecha_inicio'))} en alquiler: {alquiler_copia}")
                    continue

                if isinstance(alquiler_copia.get('fecha_fin'), str):
                    try:
                        alquiler_copia['fecha_fin'] = datetime.fromisoformat(alquiler_copia['fecha_fin'])
                    except ValueError:
                        print(f"ADVERTENCIA MIS_ALQUILERES: Formato de fecha_fin inválido en alquiler: {alquiler_copia}")
                        continue
                elif not isinstance(alquiler_copia.get('fecha_fin'), datetime):
                    print(f"ADVERTENCIA MIS_ALQUILERES: Tipo de fecha_fin inesperado: {type(alquiler_copia.get('fecha_fin'))} en alquiler: {alquiler_copia}")
                    continue

                mis_alquileres_filtrados.append(alquiler_copia)
            # else: # DEBUG Opcional
                # print(f"DEBUG MIS_ALQUILERES: Alquiler no coincide. Email del alquiler: {alq.get('email')}")

        motos = obtener_motos()

        gasto_total = 0
        for alquiler_obj in mis_alquileres_filtrados:
            gasto_total += float(alquiler_obj.get('precio_total', 0))

        # --- Ordenar manualmente por fecha_inicio (descendente - más reciente primero) ---
        # Algoritmo de ordenación por selección (o similar a burbuja para este caso)
        n = len(mis_alquileres_filtrados)
        for i in range(n):
            for j in range(0, n - i - 1):
                # Para ordenar de más reciente a más antiguo (descendente)
                # intercambiar si el elemento actual (j) es ANTERIOR (menor) al siguiente (j+1)
                fecha_j = mis_alquileres_filtrados[j].get('fecha_inicio')
                fecha_j_mas_1 = mis_alquileres_filtrados[j+1].get('fecha_inicio')

                # Asegurarse de que ambas fechas sean objetos datetime para la comparación
                # Esto ya debería estar garantizado por la conversión anterior, pero es una buena verificación.
                if isinstance(fecha_j, datetime) and isinstance(fecha_j_mas_1, datetime):
                    if fecha_j < fecha_j_mas_1: # Si la actual es menos reciente que la siguiente
                        mis_alquileres_filtrados[j], mis_alquileres_filtrados[j+1] = mis_alquileres_filtrados[j+1], mis_alquileres_filtrados[j]
                elif fecha_j is None and fecha_j_mas_1 is not None: # Considerar None como el más antiguo
                    # No hacer nada, None ya está "antes"
                    pass
                elif fecha_j is not None and fecha_j_mas_1 is None: # Considerar None como el más antiguo
                     mis_alquileres_filtrados[j], mis_alquileres_filtrados[j+1] = mis_alquileres_filtrados[j+1], mis_alquileres_filtrados[j]


        print(f"DEBUG MIS_ALQUILERES: Alquileres filtrados y ordenados para el usuario: {mis_alquileres_filtrados}")

        return render_template(
            'mis_alquileres.html',
            alquileres=mis_alquileres_filtrados, # Pasar la lista ya filtrada y ordenada
            motos=motos,
            gasto_total=gasto_total
        )