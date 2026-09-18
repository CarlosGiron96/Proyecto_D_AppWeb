from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre o Razón Social', validators=[
        DataRequired(message="El nombre del cliente es requerido."),
        Length(min=3, max=100)
    ])
    ciudad = StringField('Ciudad', validators=[
        DataRequired(message="Ingrese la ciudad del cliente.")
    ])
    contacto = StringField('Teléfono de Contacto', validators=[
        DataRequired(message="El teléfono es obligatorio."),
        Length(min=9, max=10, message="El número telefónico debe tener entre 9 y 10 dígitos.")
    ])
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message="El correo electrónico es requerido."),
        Email(message="Ingrese un correo electrónico válido.")
    ])
    submit = SubmitField('Guardar Cliente')