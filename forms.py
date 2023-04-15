from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app import User


class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur :',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email :',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe :', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmez le mot de passe :',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S\'inscrire')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet e-mail est pris. Veuillez en choisir un autre.')


class LoginForm(FlaskForm):
    email = StringField('Email :',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe :', validators=[DataRequired()])
    submit = SubmitField('Se Connecter')
