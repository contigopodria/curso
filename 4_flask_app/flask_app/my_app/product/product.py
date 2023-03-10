# Importamos módulos necesarios
from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
from my_app import db, rol_admin_need, ALLOWED_EXTENSIONS_FILES, app
from my_app.product.model.products import PRODUCTS
from my_app.product.model.product import Product, ProductForm
from my_app.product.model.category import Category
from sqlalchemy.sql.expression import not_, or_
#from flask_paginate import Pagination, get_page_parameter
from flask_login import login_required
import os


product = Blueprint('product', __name__)

# Ésta función lo que hace es requerir que el usuario esté logueado para que todas las funciones de éste archivo se realicen
@product.before_request
@login_required
@rol_admin_need
def constructor():
    pass

def allowed_extensions_file(filename):
    return ('.' in filename and filename.lower().rsplit('.')[1] in ALLOWED_EXTENSIONS_FILES)

# Ruta de inicio = index
@product.route('/')
def index():
    return render_template('product/index.html')

# Lista de productos
@product.route('/products')
#@product.route('/product/<int:page>')
def products():
    products = Product.query.all()
    #if page > 1:
        #for page_num in pagination.iter_pages():
            #paginas = (page_num)
    #else:
        #paginas = page
    return render_template('product/products.html', products=products)


@product.route('/product/<int:id>')
def show(id):
    product = Product.query.get_or_404(id)
    return render_template('product/show.html', product=product)

# Eliminar un producto
@product.route('/product-delete/<int:id>')
def delete(id):
    # PRIMERO Conseguir el registro si existe
    product = Product.query.get_or_404(id)
    # Borramos a la session de la db la variable
    db.session.delete(product)
    # Lo confirmamos para que realiza el cambio en la base de datos
    db.session.commit()
    # Mensaje
    flash('Producto eliminado')
    # Redirigimos a la lista index
    return redirect(url_for('product.products'))

# Crear un producto
@product.route('/product-create', methods=['GET', 'POST'])
def create():
    form = ProductForm()  # meta={'csrf': False}
    categories = [(c.id, c.name) for c in Category.query.all()]
    form.category_id.choices = categories
    if form.validate_on_submit():
        p = Product(request.form['name'],
                    request.form['price'], request.form['category_id'])
        # Obtener la sesión de la base y con el método add registramos el  producto
        db.session.add(p)
        # Llammamos al commit de la sesión de la base de datos para que surjan los cambios
        db.session.commit()
        # Creamos mensaje de creación exitosa
        flash('Producto creado con éxito')
        return redirect(url_for('product.products'))
    if form.errors:
        flash(form.errors.items(), 'form-error')
    return render_template('product/create.html', form=form)

# Actualizar un producto
@product.route('/product-update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Variable producto
    product = Product.query.get_or_404(id)
    form = ProductForm()  # meta={'csrf': False}
    categories = [(c.id, c.name) for c in Category.query.all()]
    form.category_id.choices = categories
    if request.method == 'GET':
        form.name.data = product.name
        form.price.data = product.price
        form.category_id.data = product.category_id
        form.file.data = product.file
        form.id.data = product.id
    if form.validate_on_submit():
        # Actualizar el producto
        product.name = form.name.data
        product.price = form.price.data
        product.category_id = form.category_id.data
        # Se comprueba si la extensión del archivo es válida
        file = form.file.data
        if file:
            if allowed_extensions_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                product.file = filename
        else:
            if product.file and file == None:
                filename = product.file
                product.file = filename
            elif file == None:
                filename = '0.jpg'
                product.file = filename
        # Obtener la sesión de la base y con el método add registramos el  producto
        db.session.add(product)
        # Llammamos al commit de la sesión de la base de datos para que surjan los cambios
        db.session.commit()
        # Creamos mensaje de creación exitosa
        flash('Producto actualizado con éxito')
        return redirect(url_for('product.products'))
    # Si hay algún error nos lo muestra
    if form.errors:
        flash(form.errors.items(), 'form-error')
    return render_template('product/update.html', product=product, form=form)


@product.route('/test')
def test():
    # p = Product.query.limit(2).all()
    # p = Product.query.first()
    # p = Product.query.order_by(Product.id.desc()).limit(2).all()
    # p = Product.query.get({'id': 1})
    # p = Product.query.filter_by(name='Producto 1').first()
    # p = Product.query.filter(Product.id>1).all()
    # p = Product.query.filter_by(name='Producto 1', id=1 ).first()
    # p = Product.query.filter(Product.name.like('Producto %')).all()
    # p = Product.query.filter(not_(Product.id > 3)).all()
    # p = Product.query.filter(or_(Product.id > 3, Product.name == 'Producto 2')).all()
    # print(p)

    # Crear un registro
    # p = Product('Producto 5', 60.8)
    # db.session.add(p)
    # db.session.commit()

    # Actualizar un registro
    # PRIMERO Conseguir el registro
    # p = Product.query.get({'id': 5})
    # Le damos el parámetro que queremos actualizar en éste caso el nombre que es p.name y se llamará Producto 5 Actualizado
    # p.name = 'Producto 5 Actualizado'
    # Añadimos a la session de la db la variable
    # db.session.add(p)
    # Lo confirmamos para que realiza el cambio en la base de datos
    # db.session.commit()

    # Borrar un registro
    # PRIMERO Conseguir el registro
    p = Product.query.get({'id': 5})
    # Borramos a la session de la db la variable
    db.session.delete(p)
    # Lo confirmamos para que realiza el cambio en la base de datos
    db.session.commit()
    return 'Flask test'

# Rutas para filtrar
@product.route('/filter/<int:id>')
def filter(id):
    product = Product.query.get(id)
    return render_template('product/filter.html', product=product)
@product.app_template_filter('iva')
def iva_filter(product):
    if product['price']:
        return product['price']*.21+product['price']
    return "Sin precio"
