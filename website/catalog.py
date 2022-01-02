from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
import tmdbsimple as tmdb

tmdb.API_KEY = 'f2cba5229db26a4e1e3e1a90409d363d'


catalog = Blueprint('catalog', __name__)


@catalog.route('/movies')
def movies():
    return redirect(url_for('catalog.popular_movies'))


@catalog.route('/movies/popular')
def popular_movies():
    movies_list = tmdb.Movies().popular()['results']
    return render_template("movies.html", user=current_user, movies=movies_list)


@catalog.route('/movies/<int:movie_id>')    # int: only integer will be passed in the url otherwise it will give a 404 error
def movie(movie_id):
    movie = tmdb.Movies(movie_id)
    cr = movie.credits()
    return render_template("movie.html", user=current_user, movie=movie, tmdb=tmdb)