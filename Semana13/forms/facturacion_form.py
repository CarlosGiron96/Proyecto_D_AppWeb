from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FacturacionForm(FlaskForm):
    cliente = StringField('Nombre del Cliente', validators=[
        DataRequired(message="Seleccione o escriba el cliente.")
    ])
    fecha = DateField('Fecha de Emisión', validators=[
        DataRequired(message="Ingrese la fecha de emisión.")
    ])
    total = DecimalField('Monto Total ($)', validators=[
        DataRequired(message="Ingrese el monto total."),
        NumberRange(min=0.01, message="El monto debe ser superior a $0.00")
    ])
    estado = SelectField('Estado de la Factura', choices=[
        ('Pagada', 'Pagada'),
        ('Pendiente', 'Pendiente'),
        ('Anulada', 'Anulada')
    ], validators=[DataRequired()])
    submit = SubmitField('Procesar Factura')