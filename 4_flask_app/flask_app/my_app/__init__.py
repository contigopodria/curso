# Importar módulos necesarios
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
from functools import wraps

app = Flask(__name__)

app.config.from_object('configuration.DevelopmentConfig')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/pyalmacen'
db = SQLAlchemy(app)

# Creamos el loginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "fauth.login"


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


from my_app.product.product import product
from my_app.product.category import category
# from my_app.auth.views import auth
from my_app.fauth.views import fauth
# Importar las vistas
app.register_blueprint(product)
app.register_blueprint(category)
#app.register_blueprint(auth)
app.register_blueprint(fauth)

with app.app_context():
    db.create_all()


@app.template_filter('mydouble')
def mydouble_filter(n:float):
    if n:
        return n*2
    return "Sin valor"


