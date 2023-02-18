# Importar lo necesario
from my_app import app
from flask import render_template
from sqlalchemy.exc import DataError


@app.errorhandler(400)
def handle_csrf_error(e):
    return render_template('general/400.html', e=e.description)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('general/404.html',e=e.description)

@app.errorhandler(Exception)
def error_server(e):
    return render_template('general/500.html', e=e.description)
