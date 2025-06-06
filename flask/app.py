'''
Importacion inicial del framework flask como principal para la app.py y pueda arrancar,
en las demas rutas se definio otros sucesores que son parte de flask incluido en su paquete pip,
para tener un mejor orden de este codigo y solo importar los codigos divididos en la carpeta routes (rutas en español 🙄)
asi pues logramos tener un codigo limpio y ordenado y que de este codigo que es el corazon ❤️ del proyecto
lea los from/import registrar las rutas (leerlas 🧐) y ejecutar cada parte de codigo que sea necesario o solicitado segun
lo que estemos haciendo en la lading_page de los templates con este codigo sincronico. Se utilizo la arquitectura MVC 🥰
Pero sin la M 🙄😞 este codigo esta hecho a base de funciones 😏 vistas ya en clases de logica de programacion 🤓
mas no aun clases "(class)" aun que ya tenemos un previo conocimiento debido a las clases de analisis y diseño de sistemas pero
aun no manejamos muy bien esa parte pero ya podemos manejar las funciones (def) gracias a los ejemplos, clases, y practicas
que hemos tenido, entonces este codigo seria solo VC (View controller) que muestra las interfazes de usuarios con jinja
y como controller @app.route(...) que Recibe las solicitudes del usuario, llama a la funcion, y devuelve la vista.

Y como ultimo este proyecto a nacido de la propuesta inicial del sorteo de proyectos el cual a nosotros nos toco este sistema
el cual todos estuvimos de acuerdo de trabajarlo de esta manera aun que es algo no visto en clases
pero decidimos dar un paso mas por dicha razon de querer entregar un buen proyecto en el cual aplique todo lo visto en clases
(No solo de programacion aun que dicho proyecto trate solo de esta clase, pero decidimos aplicar todos nuestros conocimientos
adquiridos en este ciclo en todo este proyecto lo cual a su principio fue un reto pero ahora una realidad del cual
nos llevamos, {Experiencia, Conocimiento, Aprendizaje, Trabajo en equipo, Mayor manejo de errores} Y sobre todo
aplicando mayormente las funciones vistas en clases, y un buen uso de los arreglos entre otros temas vistos en clases.
att.. [Daniel Cartagena. Fernando Gonzales. Emerson Cruz])
⬇️⬇️⬇️⬇️⬇️📲👨‍💻
'''
# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
from routes.index import register_index_routes
from routes.dashboard import register_dashboard_routes
from routes.mis_alquileres import register_mis_alquileres_routes
from routes.logout import register_logout_routes
from routes.login import register_login_routes
from routes.motodb import obtener_motos
from routes.userdb import obtener_usuarios, agregar_usuario
from routes.register import register_register_routes
from routes.alquilar import register_alquilar_routes
from routes.motoview import register_motoview_routes
from routes.adminpanel import register_admin_routes
from routes.generar_datos import register_generador_routes
from routes.adminpanel import abreviar
# from routes.alquileresdb import guardar_alquiler  # Solo si la voy a usar pero parece ya no util

app = Flask(__name__)
app.jinja_env.filters['abreviar'] = abreviar
app.secret_key = 'moto_rental_secret_key'

# Agregar un usuario de ejemplo
agregar_usuario('juan', {
    'password': '123456',
    'nombre': 'Juan Pérez',
    'email': 'juan@example.com'
})

# Registro de rutas
register_index_routes(app)
register_dashboard_routes(app)
register_mis_alquileres_routes(app)
register_logout_routes(app)
register_login_routes(app)
register_register_routes(app)
register_alquilar_routes(app)
register_motoview_routes(app)
register_admin_routes(app)
register_generador_routes(app)

# Cargar datos iniciales si realmente es necesario
motos = obtener_motos()
usuarios = obtener_usuarios()
# alquileres = obtener_todos_los_alquileres()  # igualmente que lo anterior pero ya no me es tan util

@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.html'), 404

@app.context_processor
def utility_processor():
    return dict(now=datetime.now)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

