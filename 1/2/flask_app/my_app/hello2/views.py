# Importamos módulos necesarios
from my_app import app



@app.route('/hello1')
def hello1():
    return "Hola mundo 1"