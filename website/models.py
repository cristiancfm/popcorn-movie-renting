from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))


class RentedMovie(db.Model, UserMixin):
    __tablename__ = 'rented_movies'
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    movieId = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    returnDate = db.Column(db.Date)


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
