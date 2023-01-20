# Importar módulos necesarios
from flask import Flask
from my_app.hello1.views import hello
from my_app.hello2.views import hello2

app = Flask(__name__)
app.register_blueprint(hello)
app.register_blueprint(hello2)
# Importar las vistas
#import my_app.hello1.views
#import my_app.hello2.views