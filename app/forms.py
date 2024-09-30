from flask_wtf import FlaskForm

from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user

from wtforms import SelectField, DateField, IntegerField, StringField, PasswordField, BooleanField, SubmitField, DateField, TimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp, NumberRange
from wtforms import TextAreaField
from wtforms.validators import Length

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

import sqlalchemy as sa

from app import db, photos
from app.models import User, Pet
from datetime import datetime, date, time

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
    

class PossibleWalkForm(FlaskForm):
    max_pets = IntegerField('Número máximo de pets', validators = [DataRequired(),
        NumberRange(min=1, message="O número deve ser maior ou igual a 1.")])
    date = DateField('Data para a caminhada', validators = [DataRequired()])
    start_hour = TimeField('Horário de inicio da caminhada', format='%H:%M', validators=[DataRequired()])
    end_hour = TimeField('Horário de término da caminhada', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def validate_date(self, field):
        if field.data < date.today():
            raise ValidationError("A data não pode ser anterior ao dia de hoje.")

    def validate_end_hour(self, field):
        if self.start_hour.data and field.data:
            if field.data <= self.start_hour.data:
                raise ValidationError("O horário de término deve ser após o horário de início.")

class PetForm(FlaskForm):
    name = StringField('Pet name', validators = [DataRequired()])
    pet_type = SelectField(
        'Tipo de Pet',
        choices=[
            ('dog', 'Cachorro'),
            ('cat', 'Gato')
        ], validators=[DataRequired()])
    photo = FileField('Foto do pet', validators=[FileAllowed(photos, 'Somente imagens são aceitas!')])
    breed = StringField('Raça', validators = [DataRequired()])
    sex = SelectField(
        'Gênero do Pet',
        choices=[
            ('male', 'Macho'),
            ('female', 'Fêmea')
        ], validators=[DataRequired()])
    friendly = BooleanField('É amigável?', validators=[])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        # Verifica se já existe um pet com o mesmo nome e dono
        existing_pet = db.session.query(Pet).filter_by(name=name.data, username=current_user.username).first()
        if existing_pet:
            raise ValidationError('Já existe um pet com esse nome registrado para esse usuário.')

class AcceptForm(FlaskForm):
    submit = SubmitField('Aceitar')

class DeclineForm(FlaskForm):
    submit = SubmitField('Recusar')

class RequestForm(FlaskForm):
    pet = SelectField('Para qual pet você vai solicitar o serviço',choices=[], validators=[DataRequired()])
    submit = SubmitField('Solicitar Serviço')

    def __init__(self, pets=None):
        super().__init__()  # calls the base initialisation and then...
        if pets: 
            self.pet.choices = [(pet.name, pet.name) for pet in pets]
