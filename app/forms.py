from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp
import sqlalchemy as sa
from app import db
from app.models import User
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')
    phone = StringField(
        'Phone', validators=[DataRequired(),Length(min=8, message="Minimun 8 digits.")])
    birth_date = DateField('Birth Date', format='%d-%m-%Y', default=datetime.now().strftime("%Y-%m-%d"),
                           validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Regexp(r'([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})')])


    def validate_cpf(self, cpf):
        user = db.session.scalar(sa.select(User).where(
            User.cpf == cpf.data))
        
        if user is not None:
                raise ValidationError('Cpf already registered.')
        
        cpf_string = ''.join(filter(str.isdigit, cpf.data))

        def check_digit(cpf, weight):
            sum = sum(int(cpf[i]) * (weight - i) for i in range(weight - 1))
            digit = (sum * 10) % 11
            return digit if digit < 10 else 0
        
        digit1 = check_digit(cpf_string, 10)
        
        if digit1 != int(cpf[9]):
            raise ValidationError('Invalid cpf.')
        
        digit2 = check_digit(cpf_string, 11)
        if digit2 != int(cpf[10]):
            raise ValidationError('Invalid cpf.')
        

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