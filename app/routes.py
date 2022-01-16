import flask
from flask import session
from flask import request
from app import app
from app.db_interaction import log_user
from app.db_interaction import add_user
from app.db_interaction import create_game
from app.db_interaction import connect_game

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
@app.route('/home', methods=["GET", "POST"])
def home():
    # try:
    #     if session['username'] != None:
    #         session["username"] = ""
    #         return flask.render_template('index.html')
    # except KeyError:

    # print(session['username'])
    return flask.render_template('index.html')


@app.route('/user', methods=["GET", "POST"])
def user():
    if request.method == "GET":
        try:
             if session['username'] != None:
                 data = [session['username']]
                 return flask.render_template('user.html', data=data)
        except KeyError:
            return "Please log in"
    elif request.method == "POST":
        login, passwd = request.form['name'], request.form['password']
        if log_user(login, passwd):
            session["username"] = login
            return flask.render_template('user.html')
        else:
            return "Wrong login or password"


@app.route('/register', methods=["POST"])
def register():
    login, passwd = request.form['name'], request.form['password']
    add_user(login, passwd)
    return user()


@app.route('/creategame', methods=["POST"])
def creategame():
    game_name, player_count, creator_name = request.form['name'], request.form['count'], session['username']
    create_game(game_name, player_count, creator_name)
    return request.form['name']


@app.route('/game', methods=["GET", "POST"])
def game():
    connect_game(request.form['gameid'], session['username'])
    data = ()
    # данные для отображения и разделения на этапы
    return flask.render_template('game.html')


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    return flask.render_template('index.html')
