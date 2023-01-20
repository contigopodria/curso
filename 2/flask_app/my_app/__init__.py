# Importar módulos necesarios
from flask import Flask

app = Flask(__name__)

# Importar las vistas
import my_app.hello1.views
import my_app.hello2.views