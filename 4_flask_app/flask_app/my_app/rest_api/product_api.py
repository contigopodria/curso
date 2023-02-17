# Importamos módulos necesarios
from flask.views import MethodView
from flask import request, abort
from my_app.product.model.product import Product
from my_app.product.model.category import Category
from my_app import app, db
from my_app.rest_api.helper.request import sendResJson
import json


class ProductApi(MethodView):
    # Función get
    def get(self, id=None):
        products = Product.query.all()
        if id:
           product = Product.query.get_or_404(id)
           res = productToJson(product)
        else:   
            res = []
            for p in products:
                res.append(productToJson(p))
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
        # Validación precio
        if not 'price' in request.form:
            return sendResJson(None, 'Indique el precio', 403)
        # Validación del tipo de dato del precio
        try:
            float(request.form['price'])
        except:
            return sendResJson(None, 'Introducir precio numérico', 403)
        # Validación de la categoría
        if not 'category_id' in request.form:
            return sendResJson(None, 'Indique una categoría', 403)
        # Validación del tipo de dato de la categoría
        try:
            int(request.form['category_id'])
        except:
            return sendResJson(None, 'Indique el codigo de la categoria', 403)
        # Validar que la categoría existe
        categories = Category.query.all()
        # res es una Lista
        res = []
        # Valor de la categoría  es None
        valor = None
        for c in categories:
            res.append({
                'id': c.id
            })
            # Si existe la categoría valor es verdadero
            if c.id == int(request.form['category_id']):
                valor = True
        # Si la categoría no existe el valor sigue siendo None        
        if not valor:
            return sendResJson(None, 'Indique una categoria valida', 403)
        # Crear el producto
        p = Product(request.form['name'], request.form['price'], request.form['category_id'])
        # Obtener la sesión de la base y con el método add registramos el  producto
        db.session.add(p)
        # Llammamos al commit de la sesión de la base de datos para que surjan los cambios
        db.session.commit()
        return sendResJson(productToJson(p), None, 200)

    # Función put para actualizar
    def put(self, id):
        p = Product.query.get(id)
        # Se comprueba si el producto existe
        if not p:
            print(id)
            return sendResJson(None, 'El producto no existe', 403)
        if not request.form:
            return sendResJson(None, 'Introducir datos', 403)
        # Validaciones del nombre
        if not 'name' in request.form:
            return sendResJson(None, 'Introduzca un nombre', 403)
        if len(request.form['name']) < 1:
            return sendResJson(None, 'Asigne un nombre', 403)
        # Validación precio
        if not 'price' in request.form:
            return sendResJson(None, 'Indique el precio', 403)
        # Validación del tipo de dato del precio
        try:
            float(request.form['price'])
        except:
            return sendResJson(None, 'Introducir precio numerico', 403)
        # Validación de la categoría
        if not 'category_id' in request.form:
            return sendResJson(None, 'Indique una categoria', 403)
        # Validación del tipo de dato de la categoría
        try:
            int(request.form['category_id'])
        except:
            return sendResJson(None, 'Indique el codigo de la categoria', 403)
        # Validar que la categoría existe
        categories = Category.query.all()
        # res es una Lista
        res = []
        # Valor de la categoría  es None
        valor = None
        for c in categories:
            res.append({
                'id': c.id
            })
            # Si existe la categoría valor es verdadero
            if c.id == int(request.form['category_id']):
                valor = True
        # Si la categoría no existe el valor sigue siendo None
        if not valor:
            return sendResJson(None, 'Indique una categoria valida', 403)
        # Crear el producto
        p.name = request.form['name']
        p.price = request.form['price']
        p.category_id = request.form['category_id']
        # Obtener la sesión de la base y con el método add registramos el  producto
        db.session.add(p)
        # Llammamos al commit de la sesión de la base de datos para que surjan los cambios
        db.session.commit()
        return sendResJson(productToJson(p), None, 200)

    # Función delete
    def delete(self, id):
        product = Product.query.get(id)
        # Se comprueba si el producto existe
        if not product:
            return sendResJson(None, 'El producto no existe', 403)
        # Borramos a la session de la db la variable
        db.session.delete(product)
        # Lo confirmamos para que realiza el cambio en la base de datos
        db.session.commit()
        return sendResJson('Producto eliminado', None, 200)
        
def productToJson(product: Product):
    return {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'category_id': product.category.id,
        'category': product.category.name
    }


# Vistas que corresponden a cada una de las funciones anteriormente definidas
# product_view = ProductApi.as_view('product_view')
# Protección de las vistas
api_username = 'admin'
api_password = 'admin'
def protect(f):
    def decorated(*args, **kwrgs):
        auth = request.authorization
        if api_username == auth.username and api_password == auth.password:
            return f(*args, **kwrgs)
        return abort(401)
    return decorated


product_view = protect(ProductApi.as_view('product_view'))



# GET para todos los productos y POST para crear un producto
app.add_url_rule('/api/products/', 
view_func=product_view, 
methods=['GET', 'POST'])

# Localizar producto por id
app.add_url_rule('/api/products/<int:id>',
view_func=product_view,
methods=['GET', 'DELETE', 'PUT'])
