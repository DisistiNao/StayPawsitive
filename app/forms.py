from flask_wtf import FlaskForm

from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp
from wtforms import TextAreaField
from wtforms.validators import Length

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

import sqlalchemy as sa
from app import db, photos
from app.models import User
from datetime import datetime, date

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')
    phone = StringField(
        'Phone', validators=[DataRequired(),Length(min=8, message="Minimun 8 digits.")])
    birthdate = DateField(
        'Birth Date',
        default=date.today())
    address = StringField('Address', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Regexp(r'([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})')])


    def validate_cpf(self, cpf):

        cpf_string = ''.join([c for c in cpf.data if c.isdigit()])


        user = db.session.scalar(sa.select(User).where(
            User.cpf == cpf_string))
        
        if user is not None:
            raise ValidationError('Cpf already registered.')
        
        
        # Verificar se o CPF tem 11 dígitos
        if len(cpf_string) != 11:
            raise ValidationError('Cpf inválido.')

        
        # Verificar se todos os dígitos são iguais (caso inválido)
        if cpf_string == cpf_string[0] * 11:
            raise ValidationError('Cpf inválido.')
        
        # Verificar o primeiro dígito verificador
        soma = sum(int(cpf_string[i]) * (10 - i) for i in range(9))
        digit1 = (soma * 10 % 11) % 10
        if digit1 != int(cpf_string[9]):
            raise ValidationError('Cpf inválido.')
        
        # Verificar o segundo dígito verificador
        soma = sum(int(cpf_string[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10
        if digito2 != int(cpf_string[10]):
            raise ValidationError('Cpf inválido.')
        
        

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')



class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    image = FileField('image', validators=[FileAllowed(photos, 'Somente imagens são aceitas!')])
    submit = SubmitField('Submit')
    
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')
    
