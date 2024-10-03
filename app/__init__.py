from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

csrf=CSRFProtect()
app = Flask(__name__)
app.config.from_object(Config)
csrf.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from flask_uploads import UploadSet, configure_uploads, IMAGES

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from app import routes, models

import sqlalchemy as sa
from app.models import User
from app import app, db


def queryAll():
    query = sa.select(User)
    users = db.session.scalars(query).all()

    for u in users:

        print(f"ID: {u.id}")
        print(f"Username: {u.username}")
        print(f"Email: {u.email}")
        print(f"Password Hash: {u.password_hash}")
        print(f"Name: {u.name}")
        print(f"Phone: {u.phone}")
        print(f"Birthdate: {u.birthdate}")
        print(f"Address: {u.address}")
        print(f"CPF: {u.cpf}")
