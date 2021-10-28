import flask
from flask import request
from app import app
from app.db_interaction import log_user
from app.db_interaction import add_user


@app.route('/')
#@app.route('/index')
@app.route('/home', methods=["GET", "POST"])
def home():
    return flask.render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    return flask.render_template('login.html')

@app.route('/user', methods=["POST"])
def user():
    login, passwd = request.form['name'], request.form['password']
    if log_user(login, passwd):
        return flask.render_template('user.html')
    else:
        return "Wrong login or password"

@app.route('/register', methods=["POST"])
def register():
    login, passwd = request.form['name'], request.form['password']
    add_user(login, passwd)
    return "Welcome " + login + "!"
