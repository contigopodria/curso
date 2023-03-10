# Importamos módulos necesarios
from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages, abort
from my_app import db, rol_admin_need#, get_locale , mail, app
from my_app.product.model.category import Category, CategoryForm
from sqlalchemy.sql.expression import not_, or_
#from flask_paginate import Pagination, get_page_parameter
from flask_login import login_required
#from flask_babel import gettext
#from flask_mail import Message

from collections import namedtuple

category = Blueprint('category', __name__)

# Ésta función lo que hace es requerir que el usuario esté logueado para que todas las funciones de éste archivo se realicen
@category.before_request
@login_required
@rol_admin_need
def constructor():
    pass


@category.route('/categories')
#@category.route('/category/<int:page>')
def index():
    #pagination = Category.query.paginate(page=page, per_page=6)
    categories = Category.query.all()
    # gettext('name')
    # gettext('save')
    # gettext('created')
    # gettext('update')
    # gettext('delete')

    # print(gettext('save'))
    # print(get_locale())

#---------------------------------------------------------------------------------
    # Importamos Message desde flask_mail y definimos msg
    #msg = Message('Hola flask', recipients=['vye333@hotmail.com'])
    #msg.body='Hola desde correo mail flask'
    # Importamos mail desde my_app y enviamos correo
    #mail.send(msg)

    #with app.open_resource("static/imagenes/logo.png") as fp:
        
        #msg.attach("logo.png", "image/png", fp.read())
#---------------------------------------------------------------------------------
    #if page > 1:
        #for page_num in pagination.iter_pages():
            #paginas = (page_num)   
    #else:
        #paginas = page

    return render_template('category/categories.html', categories=categories)
    #return render_template('category/index.html', categories=pagination, paginas=paginas)


@category.route('/category/<int:id>')
def show(id):
    category = Category.query.get_or_404(id)
    return render_template('category/show.html', category=category)

# Eliminar una category
@category.route('/category-delete/<int:id>')
def deleteCategory(id):
    # PRIMERO Conseguir el registro si existe
    category = Category.query.get_or_404(id)
    # Borramos a la session de la db la variable
    db.session.delete(category)
    # Lo confirmamos para que realiza el cambio en la base de datos
    db.session.commit()
    # Mensaje
    flash('Categoría eliminada')
    # Redirigimos a la lista index
    return redirect(url_for('category.index'))

# Crear una category
@category.route('/category-create', methods=['GET', 'POST'])
def create():
    form = CategoryForm()  # meta={'csrf': False}
    if form.validate_on_submit():
        p = Category(request.form['name'])
        # Obtener la sesión de la base y con el método add registramos el  categoryo
        db.session.add(p)
        # Llammamos al commit de la sesión de la base de datos para que surjan los cambios
        db.session.commit()
        # Creamos mensaje de creación exitosa
        flash('Categoría creada con éxito')
        return redirect(url_for('category.index'))
    if form.errors:
        flash(form.errors.items(), 'form-error')
    return render_template('category/create.html', form=form)

# Actualizar una categoría
@category.route('/category-update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Variable categoría
    category = Category.query.get_or_404(id)

    group = namedtuple('Group', ['countryCode', 'phoneCode', 'phone'])

    g1 = group('+34', '96', '2820488')
    g2 = group('+30', '92', '2720488')
    g3 = group('+18', '968', '5489317')

    phones = {'phones': [g1, g2, g3]}

    form = CategoryForm(data=phones)  # meta={'csrf': False}

    #del form.telefono

    # Creo una categoría de prueba
    #c = Category(name = 'Categoria 4')

    if request.method == 'GET':
        form.name.data = category.name
        form.id.data = category.id
    if form.validate_on_submit():
        # Actualizar el categoryo
        category.name = form.name.data

        # Así se envían todos los datos del formulario
        #form.populate_obj(c)
        #print(c.name)

        # Obtener la sesión de la base y con el método add registramos el  categoryo
        db.session.add(category)
        # Llammamos al commit de la sesión de la base de datos para que surjan los cambios
        db.session.commit()
        # Creamos mensaje de creación exitosa
        flash('Categoría actualizada con éxito')
        return redirect(url_for('category.index', id=category.id))
    if form.errors:
        flash(form.errors.items(), 'form-error')

    return render_template('category/update.html', category=category, form=form)


@category.route('/test')
def test():
    # p = Category.query.limit(2).all()
    # p = Category.query.first()
    # p = Category.query.order_by(Category.id.desc()).limit(2).all()
    # p = Category.query.get({'id': 1})
    # p = Category.query.filter_by(name='Categoryo 1').first()
    # p = Category.query.filter(Category.id>1).all()
    # p = Category.query.filter_by(name='Categoryo 1', id=1 ).first()
    # p = Category.query.filter(Category.name.like('Categoryo %')).all()
    # p = Category.query.filter(not_(Category.id > 3)).all()
    # p = Category.query.filter(or_(Category.id > 3, Category.name == 'Categoryo 2')).all()
    # print(p)

    # Crear un registro
    # p = Category('Categoryo 5', 60.8)
    # db.session.add(p)
    # db.session.commit()

    # Actualizar un registro
    # PRIMERO Conseguir el registro
    # p = Category.query.get({'id': 5})
    # Le damos el parámetro que queremos actualizar en éste caso el nombre que es p.name y se llamará Categoryo 5 Actualizado
    # p.name = 'Categoryo 5 Actualizado'
    # Añadimos a la session de la db la variable
    # db.session.add(p)
    # Lo confirmamos para que realiza el cambio en la base de datos
    # db.session.commit()

    # Borrar un registro
    # PRIMERO Conseguir el registro
    p = Category.query.get({'id': 5})
    # Borramos a la session de la db la variable
    db.session.delete(p)
    # Lo confirmamos para que realiza el cambio en la base de datos
    db.session.commit()
    return 'Flask test'


@category.route('/filter/<int:id>')
def filter(id):
    category = Category.query.get(id)
    return render_template('category/filter.html', category=category)


@category.app_template_filter('iva')
def iva_filter(category):
    if category['price']:
        return category['price']*.21+category['price']
    return "Sin precio"
