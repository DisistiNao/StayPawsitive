from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
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
