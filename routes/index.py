from flask import render_template
from routes.motodb import obtener_motos


def register_index_routes(app):
    @app.route('/')
    def index():
      motos = obtener_motos()

      return render_template('index.html', motos=motos)