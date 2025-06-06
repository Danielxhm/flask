from flask import render_template, flash, session, request, redirect, url_for
from routes.userdb import obtener_usuarios
from routes.motodb import obtener_motos


def register_dashboard_routes(app):
  @app.route('/dashboard')
  def dashboard():
    usuarios = obtener_usuarios()
    motos = obtener_motos()
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

