from flask import render_template, flash, session, request, redirect, url_for
from routes.userdb import obtener_usuarios


def register_login_routes(app):
  @app.route('/login', methods=['GET', 'POST'])
  def login():
      usuarios = obtener_usuarios()
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