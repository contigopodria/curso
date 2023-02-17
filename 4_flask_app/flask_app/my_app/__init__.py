# Importar módulos necesarios
from flask import Flask, redirect, url_for
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
from functools import wraps
#from flask_cors import CORS
import os

# Creamos aplicación
app = Flask(__name__)
# Protegemos la aplicación
#CSRFProtect(app)
# Variable indica tipo de archivos a subir
ALLOWED_EXTENSIONS_FILES = set(['pdf', 'jpg', 'jpeg'])
# Configuración de la carpeta donde se subirán archivos
app.config['UPLOAD_FOLDER'] = os.path.realpath('.')+'/my_app/static/uploads'
#cors = CORS(app, resources={
            #r'/api/*': {'origins': 'http://192.168.1.14:8080'}})


# Configuración del tipo de desarrollo o producción
app.config.from_object('configuration.DevelopmentConfig')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/pyalmacen'
# Importamos la base de datos
db = SQLAlchemy(app)

# Creamos el loginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "fauth.login"

# Rol que tiene el usuario por defecto
def rol_admin_need(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if current_user.rol.value != 'admin':
            logout_user()
            return redirect(url_for('fauth.login'))
            #login_manager.unauthorized()
            #return 'Tu debes ser administrador ', 403
            #print('El rol del usuario es '+str(current_user.rol.value))
        return f(*args, **kwds)
    return wrapper

# Importar de blueprints
from my_app.product.product import product
from my_app.product.category import category
from my_app.spavue.views import spavue
# from my_app.auth.views import auth
from my_app.fauth.views import fauth

# Rest-api
from my_app.rest_api.product_api import product_view
from my_app.rest_api.category_api import category_view

# General
import my_app.general.error_handle

# Registrar las vistas
app.register_blueprint(product)
app.register_blueprint(category)
#app.register_blueprint(auth)
app.register_blueprint(fauth)
app.register_blueprint(spavue)

with app.app_context():
    db.create_all()


@app.template_filter('mydouble')
def mydouble_filter(n:float):
    if n:
        return n*2
    return "Sin valor"


