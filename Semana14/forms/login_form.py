from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message="El usuario es requerido")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="La contraseña es requerida")])
    submit = SubmitField('Iniciar Sesión')