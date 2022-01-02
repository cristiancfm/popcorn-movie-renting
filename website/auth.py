from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, RentedMovie, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import datetime as DT
import tmdbsimple as tmdb

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Please try again.', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('The email must have at least 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('The first name must have at least 2 characters.', category='error')
        elif len(lastName) < 2:
            flash('The last name must have at least 2 characters.', category='error')
        elif password1 != password2:
            flash('The passwords do not match.', category='error')
        elif len(password1) < 6:
            flash('The password must have at least 6 characters.', category='error')
        else:
            new_user = User(email=email, firstName=firstName, lastName=lastName,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)


@auth.route('/profile')
@login_required
def profile():
    rented_movies = RentedMovie.query.filter_by(userId=current_user.id).all()
    print(rented_movies[0])
    return render_template("profile.html", user=current_user, rented_movies=rented_movies, tmdb=tmdb)


@auth.route('/rent/<int:movie_id>')
@login_required
def rent(movie_id):
    rented_movie = RentedMovie.query.filter_by(movieId=movie_id).first()

    if rented_movie:
        flash('This movie was already rented.', category='error')

    else:
        today = DT.date.today()
        fifteen_days = today + DT.timedelta(days=15)

        new_rented_movie = RentedMovie(userId=current_user.id, movieId=movie_id, returnDate=fifteen_days)
        db.session.add(new_rented_movie)
        db.session.commit()
        flash('Movie rented!', category='success')

    return redirect(url_for('catalog.movie', movie_id=movie_id))


@auth.route('/login/admin', methods=['GET', 'POST'])
def login_admin():

    ADMIN_EMAIL = "admin@popcorn-renting.com"
    ADMIN_PASSWORD = "admin"

    admin = Admin.query.filter_by(email=ADMIN_EMAIL).first()
    if not admin:
        # create administrator
        new_admin = Admin(email=ADMIN_EMAIL, password=generate_password_hash(ADMIN_PASSWORD, method='sha256'))
        db.session.add(new_admin)
        db.session.commit()


    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        admin = Admin.query.filter_by(email=email).first()
        if admin:
            if check_password_hash(admin.password, password):
                flash('Logged in successfully!', category='success')
                login_user(admin, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Please try again.', category='error')
        else:
            flash('No administrator registered with this email', category='error')

    return render_template("login_admin.html", user=current_user)


