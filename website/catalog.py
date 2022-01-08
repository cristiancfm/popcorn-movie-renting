from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .models import Movie, RentedMovie
import tmdbsimple as tmdb

tmdb.API_KEY = 'f2cba5229db26a4e1e3e1a90409d363d'


catalog = Blueprint('catalog', __name__)


@catalog.route('/movies')
def movies():
    return redirect(url_for('catalog.popular_movies'))


@catalog.route('/movies/popular')
def popular_movies():
    movies_list = Movie.query.all()
    return render_template("movies.html", user=current_user, movies=movies_list, tmdb=tmdb)


@catalog.route('/movies/<int:movie_id>')    # int: only integer will be passed in the url otherwise it will give a 404 error
def movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    movie_tmdb = tmdb.Movies(movie_id)

    is_movie_rented = False
    if current_user.is_authenticated:
        rented_movies = RentedMovie.query.filter_by(userId=current_user.id).all()
        if rented_movies:   # the list has elements
            for rented_movie in rented_movies:
                if movie_id == rented_movie.movieId:
                    is_movie_rented = True

    return render_template("movie.html", user=current_user, movie=movie, movie_tmdb=movie_tmdb, is_movie_rented=is_movie_rented)
