from tkinter import CASCADE
from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    firstname = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    products = db.relationship('Product', back_populates='owner', cascade='all, delete')
    images = db.relationship('Image', back_populates='users', cascade='all, delete')
    reviews = db.relationship('Review', back_populates='users', cascade='all, delete')
    cart = db.relationship('Cart', back_populates='users', cascade='all, delete')

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname
        }

    def to_dict_user_rel(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'products': [p.to_dict_product() for p in self.products],
            'productsImages': [i.to_dict_images() for i in self.images]
        }
