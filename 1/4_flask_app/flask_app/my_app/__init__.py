# Importar módulos necesarios
from flask import Flask
from my_app.product.views import product

app = Flask(__name__)

# Importar las vistas
app.register_blueprint(product)


@app.template_filter('mydouble')
def mydouble_filter(n:float):
    if n:
        return n*2
    return "Sin valor"


