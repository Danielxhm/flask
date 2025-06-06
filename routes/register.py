from flask import render_template, flash, session, request, redirect, url_for
from routes.userdb import obtener_usuarios, agregar_usuario



def register_register_routes(app):
  @app.route('/register', methods=['GET', 'POST'])
  def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nombre = request.form['nombre']
        email = request.form['email']

        usuarios = obtener_usuarios()

        if username in usuarios:
            flash('El nombre de usuario ya existe', 'danger')
        else:
            agregar_usuario(username, {
                'password': password,
                'nombre': nombre,
                'email': email,
                'rol': 'cliente'
            })
            flash('Registro exitoso. Ahora puedes iniciar sesión', 'success')
            print("Registro OK:", obtener_usuarios())  # DEBUG
            return redirect(url_for('login'))

    return render_template('register.html')