from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Producto / Variedad', validators=[
        DataRequired(message="El nombre del producto es obligatorio."),
        Length(min=3, max=80, message="El nombre debe tener entre 3 y 80 caracteres.")
    ])
    origen = StringField('Origen / Región', validators=[
        DataRequired(message="La región de origen es obligatoria.")
    ])
    precio = DecimalField('Precio por Lote ($)', validators=[
        DataRequired(message="Ingrese un precio válido."),
        NumberRange(min=0.5, message="El precio debe ser de al menos $0.50.")
    ])
    stock = IntegerField('Stock Disponible', validators=[
        DataRequired(message="Ingrese la cantidad en stock."),
        NumberRange(min=1, message="El stock inicial debe ser mayor a 0.")
    ])
    submit = SubmitField('Guardar Producto')