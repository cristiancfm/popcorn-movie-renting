from os import error
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('The email must have at least 4 characters', category='error')
        elif len(firstName) < 2:
            flash('The first name must have at least 2 characters', category='error')
        elif password1 != password2:
            flash('The passwords do not match', category='error')
        elif len(password1) < 6:
            flash('The password must have at least 6 characters', category='error')
        else:
            flash('Account created!', category='success')


    return render_template("sign-up.html")