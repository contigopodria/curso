from my_app import db
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, HiddenField, FormField, FieldList
from wtforms.validators import InputRequired, ValidationError


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    products = db.relationship('Product', backref='category', lazy=True)
    #products = db.relationship('Product', lazy='dynamic', backref=db.backref('category', lazy='select'))
    

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Category %r' % (self.name)

# Ésta es la primera forma de chekear registro pero no se usa
def check_category2(form, field):
    res = Category.query.filter_by(name = field.data).first()
    if res:
        raise ValidationError('La Categoría %s ya existe' % field.data)

# Ésta es la forma que se usa para chekear registro
def check_category(contain=True):
    def _check_category(form, field):
        if contain:
            res = Category.query.filter(Category.name.like('%'+field.data+'%')).first()
        else:
            res = Category.query.filter(Category.name.like(field.data)).first()
        # Validación para cuando queremos CREAR un registro con el mismo nombre
        if res and form.id.data == '':
            raise ValidationError('La Categoría %s ya existe' % field.data)
        # Validación para cuando queremos ACTUALIZAR un registro y ya existe con el mismo nombre al registro que queremos actualizar
        if res and form.id.data and res.id != int(form.id.data):
            raise ValidationError('La Categoría %s ya existe' % field.data)
    return _check_category


# Clase Categoría y dentro el teléfono
class PhoneForm(FlaskForm):
    countryCode = StringField('Código país')
    phoneCode = StringField('Código teléfono')
    phone = StringField('Teléfono')


class CategoryForm(PhoneForm):
    name = StringField('Nombre', validators=[
                       InputRequired(), check_category()])
    id = HiddenField('Id')
    #recaptcha = RecaptchaField()
    #telefono = FormField(PhoneForm)
    #phones = FieldList(FormField(PhoneForm))
