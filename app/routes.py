import flask
from flask import request
from app import app
from app.db_interaction import log_user
from app.db_interaction import add_user


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/home', methods=["GET", "POST"])
def home():
    return flask.render_template('index.html')


@app.route('/login', methods=["POST"])
def login():
    login, passwd = request.form['name'], request.form['password']
    if log_user(login, passwd):
        return "Welcome " + login + "!"
    else:
        return "Wrong login or password"


@app.route('/register', methods=["POST"])
def register():
    login, passwd = request.form['name'], request.form['password']
    add_user(login, passwd)
    return "Welcome " + login + "!"
