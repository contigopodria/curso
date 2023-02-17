from my_app import db
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, ValidationError
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import InputRequired, NumberRange
from decimal import Decimal

# Tabla producto
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    file = db.Column(db.String(255))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __init__(self, name, price, category_id, file):
        self.name = name
        self.price = price
        self.category_id = category_id
        self.file = file
    
    def __repr__(self):
        return '<Product %r' % (self.name)

# Ésta es la primera forma de chekear registro pero no se usa
def check_product(form, field):
    res = Product.query.filter_by(name=field.data).first()
    if res:
        raise ValidationError('El Producto %s ya existe' % field.data)
    
# Ésta es la que se usa para chekear registro
def check_product(contain=True):
    def _check_product(form, field):
        if contain:
            res = Product.query.filter(
                Product.name.like('%'+field.data+'%')).first()
        else:
            res = Product.query.filter(Product.name.like(field.data)).first()
        # Validación para cuando queremos CREAR un registro con el mismo nombre
        if res and form.id.data == '':
            raise ValidationError('La Categoría %s ya existe' % field.data)
        # Validación para cuando queremos ACTUALIZAR un registro y ya existe con el mismo nombre al registro que queremos actualizar
        if res and form.id.data and res.id != int(form.id.data):
            raise ValidationError('La Categoría %s ya existe' % field.data)
    return _check_product

# Formulario de producto
class ProductForm(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired(), check_product()])
    price = DecimalField('Precio', validators=[InputRequired(), NumberRange(min=Decimal(0.0))])
    category_id = SelectField('Categoria', coerce=int)
    file = FileField('Archivo')  # , validators=[FileRequired()]

