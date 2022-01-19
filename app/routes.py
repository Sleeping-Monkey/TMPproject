import flask
from flask import session
from flask import request
from app import app
from app.db_interaction import log_user
from app.db_interaction import add_user
from app.db_interaction import create_game
from app.db_interaction import connect_game
from app.db_interaction import get_from_db_one_elem
from app.db_interaction import is_space_to_connect
from app.db_interaction import presents
from app.db_interaction import connected

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
@app.route('/home', methods=["GET", "POST"])
def home():
    # presents()
    return flask.render_template('index.html')


@app.route('/user', methods=["GET", "POST"])
def user():
    if request.method == "GET":
        try:
            if session['username'] != None:
                return flask.render_template('user.html')
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
    connect_game(game_name, session['username'])
    # name = get_from_db_one_elem(session['username'], "game_name", "player_list", "player_id", "-1")
    data = (game_name,)
    # данные для отображения и разделения на этапы
    return flask.render_template('game.html', data=data)
    # return request.form['name']


@app.route('/game', methods=["GET", "POST"])
def game():
    data = ()
    if not connected(session['username'], request.form['gameid']):
        # данные для отображения и разделения на этапы
        if is_space_to_connect(request.form['gameid']):
            connect_game(request.form['gameid'], session['username'])
            # данные для отображения и разделения на этапы
        else:
            data = 0
            return flask.render_template('user.html', data=data)
    name = get_from_db_one_elem(session['username'], "game_name", "player_list", "player_id", "-1")
    data = (name,)
    return flask.render_template('game.html', data=data)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    return flask.render_template('index.html')

# @app.route('discon')
