"""
Aplicación web para alquiler de motos.
Implementa funcionalidades de registro, login,
listado de motos, alquiler y gestión de usuarios.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'moto_rental_secret_key'

# Base de datos simulada (diccionarios)
usuarios = {
    'admin': {
        'password': 'admin123',
        'nombre': 'Administrador',
        'email': 'admin@motorent.com'
    }
}

# Catálogo de motos
motos = {
    1: {
        'nombre': 'KTM Adventure 390',
        'marca': 'KTM',
        'tipo': 'Aventura',
        'precio_dia': 80,
        'descripcion': 'Versátil moto de aventura ligera.',
        'descripcion_larga':
            'La KTM Adventure 390 es perfecta para los aventureros urbanos y off-road. Compacta, ágil y potente, con suspensión de largo recorrido.',
        'imagen': 'Ktm__Adventure_390.png',
        'caracteristicas': [
      '373cc',
      '44HP',
      '158kg',
      '200mm',
      '167km/h',
      'Manual'
    ]
    },
    2: {
        'nombre': 'Honda Dream 110',
        'marca': 'Honda',
        'tipo': 'Ciudad',
        'precio_dia': 30,
        'descripcion': 'Eficiente moto urbana para el día a día.',
        'descripcion_larga':
            'La Honda Dream 110 es confiable y económica. Ideal para desplazamientos diarios con bajo consumo de combustible.',
        'imagen': 'Honda__Dream_110.png',
        'caracteristicas': [
      '110cc',
      '8.6HP',
      '112kg',
      'Convencional',
      '90km/h',
      'Manual'
    ]
    },
    3: {
        'nombre': 'Suzuki VStrom 800 DE',
        'marca': 'Suzuki',
        'tipo': 'Adventure Touring',
        'precio_hora': 5,
        'precio_dia': 120,
        'descripcion': 'Moto trail potente y robusta.',
        'descripcion_larga':
            'La VStrom 800 DE combina comodidad y capacidad off-road con tecnología avanzada y excelente manejo en largos recorridos.',
        'imagen': 'Suzuki__Vstrom_800_DE_2024.png',
        'caracteristicas': [
      '776cc',
      '83HP',
      '230kg',
      '220mm',
      '191km/h',
      'Manual'
    ]
    },
    4: {
        'nombre': 'Yamaha N-Max 155',
        'marca': 'Yamaha',
        'tipo': 'Scooter',
        'precio_hora': 2.00,
        'precio_dia': 50,
        'descripcion': 'Scooter urbano con estilo moderno.',
        'descripcion_larga':
            'El Yamaha N-Max 155 ofrece un balance entre agilidad y confort, ideal para la ciudad con sistema de frenos ABS y diseño atractivo.',
        'imagen': 'Yamaha__NMAX_155_2020.png',
        'caracteristicas': [
      '155cc',
      '15HP',
      '127kg',
      'Convencional',
      '125km/h',
      'Automático'
    ]
    },
    5: {
        'nombre': 'BMW R1200GS',
        'marca': 'BMW',
        'tipo': 'Adventure',
        'precio_hora': 6.66,
        'precio_dia': 160,
        'descripcion': 'Referente mundial en motos de aventura.',
        'descripcion_larga': 'La BMW R1200GS es sinónimo de aventura sin límites. Motor potente, gran autonomía y electrónica avanzada para cualquier terreno.',
        'imagen': 'BMW__R1200GS.png',
        'caracteristicas': [
      '1170cc',
      '125HP',
      '244kg',
      '185mm',
      '210km/h',
      'Manual'
    ]
    },
    6: {
        'nombre': 'Suzuki V-Strom 650',
        'marca': 'Suzuki',
        'tipo': 'Touring',
        'precio_hora': 18.33,
        'precio_dia': 110,
        'descripcion': 'Trail versátil ideal para largos viajes.',
        'descripcion_larga': 'La Suzuki V-Strom 650 destaca por su fiabilidad y confort, perfecta para viajes largos en carretera o caminos mixtos.',
        'imagen': 'Suzuki__V-strom_650.png',
        'caracteristicas': [
      '645cc',
      '69HP',
      '213kg',
      '170mm',
      '185km/h',
      'Manual'
    ]
    },
    7: {
        'nombre': 'Ducati Diavel 1260',
        'marca': 'Ducati',
        'tipo': 'Naked/Crucero',
        'precio_hora': 7.50,
        'precio_dia': 180,
        'descripcion': 'Cruiser deportiva con alma Ducati.',
        'descripcion_larga': 'La Diavel 1260 combina potencia extrema con ergonomía cruiser. Diseño agresivo y confort para viajes rápidos.',
        'imagen': 'ducati__diavel.png',
        'caracteristicas': [
      '1262cc',
      '157HP',
      '218kg',
      '120mm',
      '270km/h',
      'Manual'
    ]
    },
    8: {
        'nombre': 'Ducati Monster 937 SP',
        'marca': 'Ducati',
        'tipo': 'Naked',
        'precio_hora': 7.0,
        'precio_dia': 170,
        'descripcion': 'La icónica Monster renovada.',
        'descripcion_larga': 'Con un diseño ligero y agresivo, la Monster 937 SP ofrece una experiencia deportiva pura con electrónica de última generación.',
        'imagen': 'Ducati__Monster_937_SP.png',
        'caracteristicas': [
      '937cc',
      '111HP',
      '186kg',
      '202mm',
      '226km/h',
      'Manual'
    ]

    },
    9: {
        'nombre': 'Ducati Streetfighter V4',
        'marca': 'Ducati',
        'tipo': 'Street/Naked',
        'precio_hora': 9.16,
        'precio_dia': 220,
        'descripcion': 'Potencia y agresividad sin carenado.',
        'descripcion_larga': 'La Streetfighter V4 es una bestia en la carretera. Tecnología de MotoGP, control total y una estética feroz.',
        'imagen': 'Ducati__Streetfighter_V4.png',
        'caracteristicas': [
      '1103cc',
      '208HP',
      '178kg',
      '120mm',
      '299km/h',
      'Manual'
    ]
    }
}


alquileres = []

@app.route('/')
def index():
    return render_template('index.html', motos=motos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in usuarios and usuarios[username]['password'] == password:
            session['username'] = username
            flash('Has iniciado sesión correctamente', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nombre = request.form['nombre']
        email = request.form['email']

        if username in usuarios:
            flash('El nombre de usuario ya existe', 'danger')
        else:
            usuarios[username] = {
                'password': password,
                'nombre': nombre,
                'email': email
            }
            flash('Registro exitoso. Ahora puedes iniciar sesión', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():

    """
    Bloque de codigo que al tocar el boton de cerrar sesion se elimine la sesion actual,
    mas sin embargo la lista de usuarios actuales registrados no se vacio solo la sesion
    """
    session.clear()  # Borra toda la sesión
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Debes iniciar sesión para acceder', 'danger')
        return redirect(url_for('login'))

    usuario_key = session['username']
    if usuario_key not in usuarios:
        session.clear()
        flash('Tu sesión ha expirado. Por favor inicia sesión nuevamente.', 'warning')
        return redirect(url_for('login'))

    filtros_marca = request.args.getlist('marca')
    filtros_tipo = request.args.getlist('tipo')
    precio_sel = request.args.get('precio')

    filtradas = {}
    for id, moto in motos.items():
        if filtros_marca and moto.get('marca') not in filtros_marca:
            continue
        if filtros_tipo and moto.get('tipo') not in filtros_tipo:
            continue
        if precio_sel:
            p = moto.get('precio_dia', 0)
            if precio_sel == '1' and p > 100: continue
            if precio_sel == '2' and (p <= 100 or p > 200): continue
            if precio_sel == '3' and p <= 200: continue
        filtradas[id] = moto

    if not filtros_marca and not filtros_tipo and not precio_sel:
        filtradas = motos

    return render_template('dashboard.html', motos=filtradas, usuario=usuarios[usuario_key])


@app.route('/moto/<int:id>')
def detalle_moto(id):
    if 'username' not in session:
        flash('Debes iniciar sesión para alquilar una moto', 'danger')
        return redirect(url_for('login'))

    if id not in motos:
        flash('Moto no encontrada', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('detalle_moto.html', moto=motos[id], id=id)

@app.route('/alquilar/<int:id>', methods=['GET', 'POST'])
def alquilar(id):
    if id not in motos:
        flash('Moto no encontrada', 'danger')
        return redirect(url_for('dashboard'))

    precio_total = 0
    unidad_tiempo = ''
    precio_por_hora = motos[id]['precio_dia'] / 24  # inicializa para que exista
    if 'username' not in session:
        flash('Debes iniciar sesión para alquilar una moto', 'danger')
        return redirect(url_for('login'))



    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        tipo_tarifa = request.form['tipo_tarifa']

        # Convertir a datetime
        fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M')
        fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M')

        duracion = fecha_fin_obj - fecha_inicio_obj

        if duracion.total_seconds() <= 0:
            flash('La fecha de fin debe ser posterior a la fecha de inicio', 'danger')
            return redirect(url_for('alquilar', id=id))

        # Calcular horas y días exactos
        horas = duracion.total_seconds() / 3600
        dias = duracion.total_seconds() / (3600 * 24)

        if tipo_tarifa == 'hora':
            if horas >= 24:
                # Si es más de un día, usar tarifa diaria
                dias_redondeado = int((horas + 23) // 24)
                precio_total = motos[id]['precio_dia'] * dias_redondeado
                unidad_tiempo = f"{dias_redondeado} días"
                precio_por_hora = motos[id]['precio_dia'] / 24
            else:
                precio_total = motos[id]['precio_hora'] * horas
                unidad_tiempo = f"{horas:.1f} horas"
                precio_por_hora = motos[id]['precio_hora']
        else:  # tarifa diaria
            dias = max(1, dias)
            precio_total = motos[id]['precio_dia'] * dias
            unidad_tiempo = f"{dias:.1f} días"
            precio_por_hora = motos[id]['precio_dia'] / 24


        # Guardar el alquiler
        alquileres.append({
            'id': len(alquileres) + 1,
            'usuario': session['username'],
            'moto_id': id,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'tipo_tarifa': tipo_tarifa,
            'precio_total': precio_total,
            'duracion': unidad_tiempo
        })

        flash(f'Moto alquilada con éxito por {unidad_tiempo}. Precio total: ${precio_total:.2f}', 'success')
        return redirect(url_for('mis_alquileres'))

    return render_template('alquilar.html', moto=motos[id], id=id, precio_total=precio_total, unidad_tiempo=unidad_tiempo, precio_por_hora=precio_por_hora)

@app.route('/mis_alquileres')
def mis_alquileres():
    """
    Muestra la lista de alquileres realizados por el usuario que ha iniciado sesión.

    Verifica que el usuario esté autenticado, filtra los alquileres
    correspondientes a ese usuario y calcula el gasto total.

    Retorna:
        Renderiza la plantilla 'mis_alquileres.html' con los datos de alquileres,
        motos y el gasto total del usuario.
    """
    if 'username' not in session:
        flash('Debes iniciar sesión para ver tus alquileres', 'danger')
        return redirect(url_for('login'))

    mis_alq = [a for a in alquileres if a['usuario'] == session['username']]

    # Calcula el gasto total
    gasto_total = sum(a['precio_total'] for a in mis_alq)

    return render_template('mis_alquileres.html', alquileres=mis_alq, motos=motos, gasto_total=gasto_total)

# Añadir esta función de contexto para la plantilla mis_alquileres.html
@app.context_processor
def utility_processor():
    return dict(now=datetime.now)

@app.errorhandler(404)
def page_not_found(_):
    """
    Manejador para error 404 - Página no encontrada.

    Renderiza la plantilla 404.html cuando una ruta no existe.
    """
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
