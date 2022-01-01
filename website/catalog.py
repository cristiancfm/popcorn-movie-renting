from flask import Blueprint, render_template
from flask_login import  login_required, current_user
import tmdbsimple as tmbd

tmbd.API_KEY = 'f2cba5229db26a4e1e3e1a90409d363d'


catalog = Blueprint('catalog', __name__)

@catalog.route('/movies')
def movies():

    popular_movies = tmbd.Movies().popular()['results']

    return render_template("movies.html", user=current_user, movies=popular_movies)
