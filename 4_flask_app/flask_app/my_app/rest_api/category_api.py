# Importamos módulos necesarios
from flask.views import MethodView
from flask import request
from my_app.product.model.product import Product
from my_app.product.model.category import Category
from my_app import app, db
from my_app.rest_api.helper.request import sendResJson
import json


class CategoryApi(MethodView):
    # Función get
    def get(self, id=None):
        categories = Category.query.all()
        if id:
           category = Category.query.get_or_404(id)
           res = categoryToJson(category)
        else:   
            res = []
            for c in categories:
                res.append(categoryToJson(c))
        return sendResJson(res, None, 200)
    # Función post
    def post(self):
        if not request.form:
            return sendResJson(None, 'Introducir datos', 403)
        # Validaciones del nombre
        if not 'name' in request.form:
            return sendResJson(None, 'Introduzca un nombre', 403)
        if len(request.form['name']) < 1:
            return sendResJson(None, 'Asigne un nombre', 403)
        # Validar que la categoría existe
        categories = Category.query.all()
        # res es una Lista
        res = []
        # Valor de la categoría  es None
        valor = None
        for c in categories:
            res.append({
                'id': c.name
            })
            # Si existe la categoría valor es verdadero
            if c.name == request.form['name']:
                valor = True
        # Si la categoría existe el valor es true        
        if valor:
            return sendResJson(None, 'La categoria ya existe', 403)
        # Crear la categoría
        c = Category(request.form['name'])
        # Obtener la sesión de la base y con el método add registramos la categoría
        db.session.add(c)
        # Llammamos al commit de la sesión de la base de datos para que surjan los cambios
        db.session.commit()
        return sendResJson(categoryToJson(c), None, 200)

    # Función put para actualizar
    def put(self, id):
        c = Category.query.get(id)
        # Se comprueba si la categoría existe
        if not c:
            return sendResJson(None, 'La categoria no existe', 403)
        if not request.form:
            return sendResJson(None, 'Introducir datos', 403)
        # Validaciones del nombre
        if not 'name' in request.form:
            return sendResJson(None, 'Introduzca un nombre', 403)
        if len(request.form['name']) < 1:
            return sendResJson(None, 'Asigne un nombre', 403)
        # Actualizar categoría
        c.name = request.form['name']
        # Obtener la sesión de la base y con el método add registramos la categoría
        db.session.add(c)
        # Llammamos al commit de la sesión de la base de datos para que surjan los cambios
        db.session.commit()
        return sendResJson(categoryToJson(c), None, 200)

    # Función delete
    def delete(self, id):
        category = Category.query.get(id)
        # Se comprueba si la categoría existe
        if not category:
            return sendResJson(None, 'La categoria no existe', 403)
        # Borramos a la session de la db la variable
        db.session.delete(category)
        # Lo confirmamos para que realiza el cambio en la base de datos
        db.session.commit()
        return sendResJson('Categoria eliminada', None, 200)
        
def categoryToJson(category: Category):
    return {
        'id': category.id,
        'name': category.name,
    }

category_view = CategoryApi.as_view('category_view')
app.add_url_rule('/api/categories/', 
view_func=category_view, 
methods=['GET', 'POST'])
app.add_url_rule('/api/categories/<int:id>',
view_func=category_view,
methods=['GET', 'DELETE', 'PUT'])
