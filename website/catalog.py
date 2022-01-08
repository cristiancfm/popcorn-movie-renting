from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .models import Movie, RentedMovie
import tmdbsimple as tmdb

tmdb.API_KEY = 'f2cba5229db26a4e1e3e1a90409d363d'


catalog = Blueprint('catalog', __name__)


@catalog.route('/movies')
def movies():
    return redirect(url_for('catalog.highest_rated_movies'))


@catalog.route('/movies/highest-rated')
def highest_rated_movies():
    def get_rating(movie_tmdb):
        return movie_tmdb['vote_average']

    # get list of movies in the database
    movies_list = Movie.query.all()

    # create list of movies and their information from TMDB
    movies_list_tmdb = []
    for movie in movies_list:
        movie_tmdb = tmdb.Movies(movie.id).info()
        movies_list_tmdb.append(movie_tmdb)
    # sort movies
    movies_list_tmdb.sort(key=get_rating, reverse=True)

    filter_by = "highest-rated"
    return render_template("movies.html", user=current_user, movies_tmdb=movies_list_tmdb, tmdb=tmdb, filter_by=filter_by)


@catalog.route('/movies/a-to-z')
def a_to_z_movies():
    def get_title(movie_tmdb):
        return movie_tmdb['title']

    # get list of movies in the database
    movies_list = Movie.query.all()

    # create list of movies and their information from TMDB
    movies_list_tmdb = []
    for movie in movies_list:
        movie_tmdb = tmdb.Movies(movie.id).info()
        movies_list_tmdb.append(movie_tmdb)
    # sort movies
    movies_list_tmdb.sort(key=get_title)

    filter_by = "a-to-z"
    return render_template("movies.html", user=current_user, movies_tmdb=movies_list_tmdb, tmdb=tmdb, filter_by=filter_by)


@catalog.route('/movie/<int:movie_id>')
def movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    movie_tmdb = tmdb.Movies(movie_id)

    is_movie_rented = False
    if current_user.is_authenticated:   # check if the movie was already rented
        rented_movies = RentedMovie.query.filter_by(userId=current_user.id).all()
        if rented_movies:   # the list has elements
            for rented_movie in rented_movies:
                if movie_id == rented_movie.movieId:
                    is_movie_rented = True

    return render_template("movie.html", user=current_user, movie=movie, movie_tmdb=movie_tmdb, is_movie_rented=is_movie_rented)
