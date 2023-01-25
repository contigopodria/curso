from my_app import db
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField
from wtforms.validators import InputRequired, NumberRange
from decimal import Decimal

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __init__(self, name, price, category_id):
        self.name = name
        self.price = price
        self.category_id = category_id
    
    def __repr__(self):
        return '<Product %r' % (self.name)

class ProductForm(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired()])
    price = DecimalField('Precio', validators=[InputRequired(), NumberRange(min=Decimal(0.0))])
    category_id = SelectField('Categoria', coerce=int)

