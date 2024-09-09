from datetime import datetime, timezone, time, date
from typing import Optional
import sqlalchemy as sa
from sqlalchemy import Date, Time, Boolean
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=False)
    phone: so.Mapped[str] = so.mapped_column(sa.String(15), index=True, unique=False)
    birthdate: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    address: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=False)
    cpf: so.Mapped[str] = so.mapped_column(sa.String(11), index=True, unique=False)
    avatar: so.Mapped[str] = so.mapped_column(sa.String(100), index=True, unique=False)
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def set_avatar(self):
        self.avatar = "avatar/placeholder.png"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def print_user(self):
        print(f"ID: {self.id}")
        print(f"Username: {self.username}")
        print(f"Email: {self.email}")
        print(f"Password Hash: {self.password_hash}")
        print(f"Name: {self.name}")
        print(f"Phone: {self.phone}")
        print(f"Birthdate: {self.birthdate}")
        print(f"Address: {self.address}")
        print(f"CPF: {self.cpf}")

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Pet(db.Model):
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.ForeignKey(User.username), index=True, primary_key=True)
    pet_type: so.Mapped[str] = so.mapped_column(sa.String(50))
    photo: so.Mapped[str] = so.mapped_column(sa.String(100))
    breed: so.Mapped[str] = so.mapped_column(sa.String(40))
    sex: so.Mapped[str] = so.mapped_column(sa.String(10))
    friendly: so.Mapped[bool] = so.mapped_column(Boolean)

    def __repr__(self):
        return "Pet name: {}\n owner:{}".format(self.name, self.username)

class PossibleWalk(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True, autoincrement=True)
    max_pets: so.Mapped[int] = so.mapped_column()
    date: so.Mapped[datetime.date] = so.mapped_column(Date)
    start_hour: so.Mapped[time] = so.mapped_column(Time)
    end_hour: so.Mapped[time] = so.mapped_column(Time)
    username: so.Mapped[str] = so.mapped_column(sa.ForeignKey(User.username), index=True)
    def __repr__(self):
        return "Possible Walk id: {}\n Possible date: {}, from {} to {}".format(self.id, self.date, self.startHour, self.endHour)
        
class PossiblePetBoarding(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True, autoincrement=True)
    max_pets: so.Mapped[int] = so.mapped_column()
    start_date: so.Mapped[date] = so.mapped_column(Date)
    end_date: so.Mapped[date] = so.mapped_column(Date)
    username: so.Mapped[str] = so.mapped_column(sa.ForeignKey(User.username), index=True)
    def __repr__(self):
        return "Possible Pet Boarding id: {}\n Possible date: from {} to {}".format(self.id, self.start_date, self.end_date)

class Service(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True, index=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(20))
    username: so.Mapped[str] = so.mapped_column(sa.ForeignKey(User.username), index=True)
    pet_name: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Pet.name))
    boarding_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(PossiblePetBoarding.id), nullable=True)
    walk_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(PossibleWalk.id),nullable=True)

    def __repr__(self):
        service_type = ""
        if self.boarding_id:
            service_type.join("Pet Boarding")
        else:
            service_type.join("Pet Walking")
        return "Service id: {}\n Service type: {}".format(self.id, service_type)
