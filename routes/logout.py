from flask import Flask, request, redirect, url_for, flash, session

def register_logout_routes(app):
  @app.route('/logout')
  def logout():

    """
    Bloque de codigo que al tocar el boton de cerrar sesion se elimine la sesion actual,
    mas sin embargo la lista de usuarios actuales registrados no se vacio solo la sesion
    """
    session.clear()  # Borra toda la sesión
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('index'))