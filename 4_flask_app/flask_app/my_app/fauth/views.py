# Importamos módulos necesarios
from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages, session, abort
from my_app.auth.model.user import LoginForm, User, RegisterForm
from flask_login import login_required
from my_app import db
from flask_login import login_user, logout_user, current_user, login_required
from my_app import login_manager

fauth = Blueprint('fauth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Crear un registro
@fauth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(meta={'csrf': False})

    if form.validate_on_submit():
        # Antes de crear el usuario se comprueba si existe
        if User.query.filter_by(username=form.username.data).first():
            flash("El usuario ya existe", 'danger')
        else:
            p = User(form.username.data, form.password.data)
            # Obtener la sesión de la base y con el método add registramos el  autho
            db.session.add(p)
            # Llammamos al commit de la sesión de la base de datos para que surjan los cambios
            db.session.commit()
            # Creamos mensaje de creación exitosa
            flash('Usuario creado con éxito')
            return redirect(url_for('fauth.login'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('auth/register.html', form=form)

# Login de usuario
@fauth.route('/login', methods=['GET', 'POST'])
def login():
    # >Comprobamos si es usuarios está atuenticado
    if current_user.is_authenticated:
        return redirect(url_for('product.index'))

    form = LoginForm(meta={'csrf': False})
    
    if form.validate_on_submit():
        # Antes de crear el usuario se comprueba si existe
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
           # Registrar la sesión
           #flash('Bienvenido de nuevo '+user.username)
           login_user(user)
           next = request.form['next']
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
           #if not is_safe_url(next):
                #return .abort(400)
           
           return redirect(next or url_for('product.index'))
        else:
            flash("Usuario o contraseña incorrectos", 'danger')
            
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('auth/login.html', form=form)

# Cerrar sesión
@fauth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('fauth.login'))

# Proteger vistas
@fauth.route('/protegido')
@login_required
def protegido():
    return 'Vista protegida'
