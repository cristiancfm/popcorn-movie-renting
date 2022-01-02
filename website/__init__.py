from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from werkzeug import Response
from werkzeug.exceptions import HTTPException
from flask_basicauth import BasicAuth

db = SQLAlchemy()
DB_NAME = "database.db"
app = Flask(__name__)
basic_auth = BasicAuth(app)

def create_app():
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    app.config['BASIC_AUTH_USERNAME'] = 'admin'
    app.config['BASIC_AUTH_PASSWORD'] = 'admin'


    db.init_app(app)

    from .views import views
    from .auth import auth
    from .catalog import catalog

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(catalog, url_prefix='/')

    from .models import User, RentedMovie, Movie

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))



    create_admin_panel(app, models)

    
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')





class MyModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())



class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())



class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))



def create_admin_panel(app, models):
    admin = Admin(app, index_view=MyAdminIndexView(), name='Popcorn Movie Renting', template_mode='bootstrap4')

    class UsersView(MyModelView):
        column_list = ['id', 'email', 'password', 'firstName', 'lastName']
        form_columns = ['id', 'email', 'password', 'firstName', 'lastName']

    class RentedMoviesView(MyModelView):
        column_list = ['userId', 'movieId', 'returnDate']
        form_columns = ['userId', 'movieId', 'returnDate']

    class MoviesView(MyModelView):
        column_list = ['id']
        form_columns = ['id']

    admin.add_view(UsersView(models.User, db.session))
    admin.add_view(RentedMoviesView(models.RentedMovie, db.session))
    admin.add_view(MoviesView(models.Movie, db.session))



