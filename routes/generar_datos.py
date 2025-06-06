from flask import render_template, flash, request
from faker import Faker
from routes.userdb import agregar_usuario, obtener_usuarios
from routes.alquileresdb import guardar_alquiler
from routes.motodb import obtener_motos
from random import choice, randint
from datetime import datetime, timedelta

def register_generador_routes(app):
    @app.route('/generar-datos', methods=['GET', 'POST'])
    def generar_datos_test():
        if request.method == 'POST':
            fake = Faker()
            motos = obtener_motos()
            cantidad_usuarios = 50
            reservas_por_usuario = 10

            usuarios_db = obtener_usuarios()
            nuevos_usuarios = 0
            nuevas_reservas = 0

            for _ in range(cantidad_usuarios):
                username = fake.unique.user_name()
                if username in usuarios_db:
                    continue

                usuario = {
                    'password': fake.password(length=10),
                    'nombre': fake.name(),
                    'email': fake.email()
                }
                agregar_usuario(username, usuario)
                nuevos_usuarios += 1

                if not motos:
                    flash('No hay motos para generar reservas.', 'danger')
                    break

                for _ in range(reservas_por_usuario):
                    moto_id = choice(list(motos.keys()))
                    precio_dia = motos[moto_id].get('precio_dia', 100)

                    fecha_inicio = fake.date_between(start_date='today', end_date='+30d')
                    duracion_dias = randint(1, 7)
                    fecha_fin = fecha_inicio + timedelta(days=duracion_dias - 1)

                    fecha_inicio_dt = datetime.combine(fecha_inicio, datetime.min.time())
                    fecha_fin_dt = datetime.combine(fecha_fin, datetime.max.time().replace(microsecond=0))

                    precio_total = precio_dia * duracion_dias

                    reserva = {
                        'username': username,
                        'email': usuario['email'],
                        'moto_id': moto_id,
                        'fecha_inicio': fecha_inicio_dt.isoformat(),
                        'fecha_fin': fecha_fin_dt.isoformat(),
                        'tipo_tarifa': 'dia',
                        'precio_total': precio_total,
                        'duracion': f"{duracion_dias} día{'s' if duracion_dias > 1 else ''}"
                    }

                    guardar_alquiler(reserva)
                    nuevas_reservas += 1

            flash(f'Se generaron {nuevos_usuarios} usuarios y {nuevas_reservas} reservas de prueba.', 'success')

        return render_template('generar_datos.html')
