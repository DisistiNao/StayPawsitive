import os
from urllib.parse import urlsplit

from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, logout_user, current_user, login_required

from werkzeug.utils import secure_filename

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app, db, photos
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PetForm, PossibleWalkForm, RequestForm, AcceptForm, DeclineForm
from app.models import User, Pet, PossibleWalk, PossiblePetBoarding, RequestedService, Service

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
            credits= 1000,
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
    
    pets = db.session.query(Pet).join(User).filter(User.username == current_user.username).all()
    
    possible_walks = db.session.query(PossibleWalk).join(User).filter(User.username == current_user.username).all()
    return render_template('user.html', user=user, age=age, phone=formatted_phone, pets=pets, possible_walks= possible_walks)

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
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/new_pet', methods=['GET', 'POST'])
@login_required
def new_pet():
    form = PetForm()

    if form.validate_on_submit():
        
        
        pet = Pet(
            name = form.name.data,
            username = current_user.username,
            pet_type = form.pet_type.data,
            photo = "petPhotos/dog_placeholder.png" if form.pet_type.data == 'dog' else "petPhotos/cat_placeholder.png",
            breed = form.breed.data,
            sex = form.sex.data,
            friendly = form.friendly.data
        )

        if form.photo.data:
            f = form.photo.data
            uploaded_filename = secure_filename(f.filename)
            _, file_extension = os.path.splitext(uploaded_filename)    
            filename = "{}_{}{}".format(current_user.username, form.name.data, file_extension)

            f.save(os.path.join(os.path.dirname(__file__),'static','petPhotos', filename))
            pet.photo = "petPhotos/{}".format(filename)
            
        db.session.add(pet)
        db.session.commit()
        flash('Seu pet foia adicionado.')
        
        return redirect(url_for('user', username=current_user.username))
    return render_template('new_pet.html', title='Regiter Pet', form=form)

@app.route('/new_walk', methods=['GET', 'POST'])
@login_required
def new_walk():
    form = PossibleWalkForm()
    if form.validate_on_submit():
        
        Session = sessionmaker(bind=db)
        session = Session()

        walk = PossibleWalk(
            max_pets = form.max_pets.data,
            date = form.date.data,
            start_hour = form.start_hour.data,
            end_hour = form.end_hour.data,
            username = current_user.username
        )

        db.session.add(walk)
        db.session.commit()
        flash('Caminhada criada!.')
        return redirect(url_for('user', username=current_user.username))
    
    return render_template('new_walk.html', title='Cadastrar Passeio',
                           form=form)



@app.route('/services/', methods=['GET', 'POST'])
@login_required
def services():

    possible_walks = db.session.query(PossibleWalk).filter(PossibleWalk.username != current_user.username).all()

    return render_template('services.html', title='Ver serviços disponíveis', possible_walks=possible_walks)


@app.route('/request_services/<type>/<id_service>', methods=['GET', 'POST'])
@login_required
def request_services(type, id_service):

    if(type == 'walk'):
        pets = db.session.query(Pet).join(User).filter(User.username == current_user.username).all()
        
        form = RequestForm(pets=pets);
        
        walk = db.session.query(PossibleWalk).filter(PossibleWalk.id == id_service).all()


        if form.validate_on_submit():
            print("REQUEST VÁLIDO")
            requested_service = RequestedService(
                username=current_user.username,
                id_service=id_service,
                status='pending'
            )

            user = current_user
            user.credits -= 1

            db.session.add(requested_service)
            db.session.commit()

            return redirect(url_for('my_services'))
        else:
            print("UAIIIIII\n")
            print(form.errors)

        return render_template('request_service.html', title='Solicitar Serviço', walk=walk, boarding=None,form=form)
    
    elif type == 'boarding':
        pets = db.session.query(Pet).join(User).filter(User.username == current_user.username).all()
        form = RequestForm(pets);
        
        form.pet.choices = [(pet.name, pet.name) for pet in pets]

        boarding = db.session.query(PossiblePetBoarding).filter(PossiblePetBoarding.id == id_service).all()

        return render_template('request_service.html', title='Solicitar Serviço', walk = None, boarding= boarding, form=form)
    
    abort(404)

@app.route('/my_services')
def my_services():

    accept_form = AcceptForm()
    decline_form = DeclineForm()

    my_requested_services = db.session.query(RequestedService).filter(User.username == current_user.username).all()

    my_services = (
        db.session.query(RequestedService)
        .join(Service, Service.id == RequestedService.id_service)
        .filter(Service.username == current_user.username)
        .filter(RequestedService.status == 'pending')
        .all()
    )
    
    if accept_form.validate_on_submit():
        service_id = accept_form.service_id.data
        requested_service = RequestedService.query.filter_by(id_service=service_id).first()

        user = User.query.filter_by(username=requested_service.username).first()
        user.credits -= 1
        requested_service.status = 'accepted'
        db.session.commit()
        
        return redirect(url_for('my_services'))
        

    elif decline_form.validate_on_submit():
        service_id = accept_form.service_id.data
        requested_service = RequestedService.query.filter_by(id_service=service_id).first()

        user = User.query.filter_by(username=requested_service.username).first()
        user.credits += 1
        requested_service.status = 'denied'
        db.session.commit()

        return redirect(url_for('my_services'))


    return render_template('my_services.html', title='Meus Serviços', my_requested_services=my_requested_services, my_services=my_services)
