# Importamos módulos necesarios
from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages, abort, session
from my_app.auth.model.user import LoginForm, User, RegisterForm
from my_app import db

auth = Blueprint('auth', __name__)

# Crear un registro
@auth.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.register'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('auth/register.html', form=form)

# Login de usuario
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(meta={'csrf': False})

    if form.validate_on_submit():
        # Antes de crear el usuario se comprueba si existe
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
           # Registrar la sesión
           session['username'] = user.username
           session['rol'] = user.rol.value
           session['id'] = user.id
           #flash('Bienvenido de nuevo '+user.username)
           return redirect (url_for('product.index'))
        else:
            flash("Usuario o contraseña incorrectos", 'danger')
            
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('auth/login.html', form=form)

# Cerrar sesión
@auth.route('/logout')
def logout():
    session.pop('username')
    session.pop('rol')
    session.pop('id')
    return redirect(url_for('auth.login'))
