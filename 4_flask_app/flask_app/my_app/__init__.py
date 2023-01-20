# Importar módulos necesarios
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object('configuration.DevelopmentConfig')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/pyalmacen'
db = SQLAlchemy(app)


from my_app.product.views import product
# Importar las vistas
app.register_blueprint(product)

with app.app_context():
    db.create_all()

@app.template_filter('mydouble')
def mydouble_filter(n:float):
    if n:
        return n*2
    return "Sin valor"


