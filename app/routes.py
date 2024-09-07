import os
from urllib.parse import urlsplit

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required

from werkzeug.utils import secure_filename
import sqlalchemy as sa

from app import app, db, photos
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User

from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            birthdate=form.birthdate.data,
            address=form.address.data,
            cpf=''.join([c for c in form.cpf.data if c.isdigit()])
        )
        user.set_avatar()
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


def calculate_age(birthdate):
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def format_phone_number(phone):
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    return phone


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user is None:
        return render_template('404.html'), 404
    
    age = calculate_age(user.birthdate)
    formatted_phone = format_phone_number(user.phone)
    
    return render_template('user.html', user=user, age=age, phone=formatted_phone)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        
        if form.username.data:
            current_user.username = form.username.data
        current_user.about_me = form.about_me.data

        if form.image.data:
            f = form.image.data
            uploaded_filename = secure_filename(f.filename)
            _, file_extension = os.path.splitext(uploaded_filename)    
            filename = "{}{}".format(current_user.username, file_extension)

            f.save(os.path.join(os.path.dirname(__file__),'static','avatar', filename))
            current_user.avatar = "avatar/{}".format(filename)

        db.session.commit()
        flash('Your changes have been saved.')

        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)