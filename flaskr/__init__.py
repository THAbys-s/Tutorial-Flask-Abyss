import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # configuración y setup...
    app.config.from_mapping(
        SECRET_KEY='SYBBAHT', #Flask lo utiliza para encriptar información importante 
        # (Entre ellos el id, usuario y contraseña. Es muy importante cambiarlo)
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path) #Instancia una carpeta en la ruta proporcionada.
    except OSError:
        pass # Si ya está creada, simplemente no hace nada.

    #Importo la conexión entre las distintas bibliotecas.
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

# Una vista es la función que retorna Flask.
