from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class ProveedorForm(FlaskForm):
    finca = StringField('Nombre de la Finca / Asociación', validators=[
        DataRequired(message="El nombre de la finca es obligatorio."),
        Length(min=4, max=100)
    ])
    region = StringField('Región de Cosecha', validators=[
        DataRequired(message="Ingrese la región de procedencia.")
    ])
    tipo_grano = SelectField('Tipo de Grano Producido', choices=[
        ('Arábigo', 'Arábigo'),
        ('Robusta', 'Robusta'),
        ('Blend', 'Blend Tradicional')
    ], validators=[DataRequired(message="Seleccione un tipo de grano.")])
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="Ingrese el teléfono de contacto."),
        Length(min=9, max=10)
    ])
    submit = SubmitField('Guardar Proveedor')