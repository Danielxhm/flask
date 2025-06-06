from flask import render_template, flash, session, request, redirect, url_for
from routes.userdb import obtener_usuarios
from routes.motodb import obtener_motos

def register_motoview_routes(app):
  @app.route('/moto/<int:id>')
  def detalle_moto(id):
    usuarios = obtener_usuarios()
    motos = obtener_motos()
    if 'username' not in session:
        flash('Debes iniciar sesión para alquilar una moto', 'danger')
        return redirect(url_for('login'))

    if id not in motos:
        flash('Moto no encontrada', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('detalle_moto.html', moto=motos[id], id=id)