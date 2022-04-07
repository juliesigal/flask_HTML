from flask import Flask, redirect, render_template, request, url_for, session, Response, jsonify, make_response
import jwt
import json
import uuid
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_session import Session


from Users import Users
from db_config import local_session
from db_repo import DbRepo
from logger import Logger

# creates Flask object
app = Flask(__name__)
repo = DbRepo(local_session)
logger = Logger.get_instance()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'Julie Sigal'
# Session(app)


@app.route("/")
def home():
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if 'remember' in session:
            return redirect(url_for('my_app'))
        return render_template('signup.html')
    form_data = request.form
    # gets name, email and password from request
    _username = form_data.get('username')
    print(_username)
    _email = form_data.get('email')
    print(_email)
    _password = form_data.get('psw')
    print(_password)

    # check if user exists in db
    user = repo.get_user_by_username(_email)
    print(user)
    # ...
    if user:
        return make_response('User already exists. Please Log in.', 202)
    else:
        pw = generate_password_hash(_password, method='sha256')
        # create new user
        new_user = Users(public_id=str(uuid.uuid4()), username=_username, email=_email,
                     password=pw)
        repo.post_user(new_user)
        return render_template('my_app.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'remember' in session:  # checking if the user wants to rememeber him
            return redirect(url_for("my_app.html"))
        return render_template('login.html')
    if request.method == 'POST':
        form_data = request.form
        # check that no field is missing
        if not form_data.get('uname') or not form_data.get('psw'):
            return make_response('Could not verify', 401,
                                 {'WWW-Authenticate': 'Basic realm ="Login required!"'})
        # check if user exists in db
        user = repo.get_user_by_username(form_data.get('uname'))
        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="User does not exist!"'})
        # check password
        if not check_password_hash(user[0].password, form_data.get('psw')):
            return make_response('Could not verify', 403, {'WWW-Authenticate': 'Basic realm ="Wrong Password!"'})
        session['user'] = user[0].username
        if 'remember' in request.form:  # checking if the user clicked on "remember me" check box
            session['remember'] = True
            return render_template('my_app.html')
        else:
            return render_template('my_app.html')

@app.route("/my_app")
def my_app():
    if 'user' in session:
        user = session['user']
        return render_template('my_app.html', user=user)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if 'user' in session:  # removing "user" from the session
        session.pop('user')
    if 'remember' in session:  # removing "remember" from the session
        session.pop('remember')
    return redirect(url_for("login"))

if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debuger shell
    # if you hit an error while running the server
    app.run(debug=True, port=5002)
