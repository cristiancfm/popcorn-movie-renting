from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    firstName = db.Column(db.String(150), nullable=False)
    lastName = db.Column(db.String(150), nullable=False)


class RentedMovie(db.Model, UserMixin):
    __tablename__ = 'rented_movies'
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    movieId = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    returnDate = db.Column(db.Date, nullable=False)


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
