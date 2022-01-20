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
from app.db_interaction import stage_change
from app.db_interaction import is_gave
from app.db_interaction import pr_gave
from app.db_interaction import set_grades
from app.game_logic import appoint_recipient

from sys import stderr

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
@app.route('/home', methods=["GET", "POST"])
def home():
    # presents()
    return flask.render_template('index.html')


@app.route('/user', methods=["GET", "POST"])
def user():
    data = []
    if request.method == "GET":
        try:
            if session['username'] != None:
                games = get_from_db_one_elem(session['username'], "*", "player_list", "player_id", "-1")
                for i in range(len(games)):
                    data.append(games[i][1])
                return flask.render_template('user.html', data=data)
        except KeyError:
            return "Please log in"
    elif request.method == "POST":
        login, passwd = request.form['name'], request.form['password']
        if log_user(login, passwd):
            session["username"] = login
            games = get_from_db_one_elem(session['username'], "*", "player_list", "player_id", "-1")
            for i in range(len(games)):
                data.append(games[i][1])
            return flask.render_template('user.html', data=data)
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
def game():#конекта к разным играм нет, потому что нельзя из базы брать один элемент
#, когда пользователь может создавать много...
    game_name = get_from_db_one_elem(session['username'], "game_name", "player_list", "player_id", "-1")
    if request.args.get("a") == "1":
        pr_gave(session['username'], game_name)
    elif request.form['gameid']: #заглушка
        game_name = request.form['gameid']
    stage = get_from_db_one_elem(game_name, "stage", "game_info", "game_name")
    data = [game_name, stage]
    if not connected(session['username'], game_name):
        if is_space_to_connect(game_name):
            connect_game(game_name, session['username'])
        else:
            data = 0
            return flask.render_template('user.html', data=data)
    if stage == 0 and not is_space_to_connect(game_name):
        #тут, когда смена состояний, должно в базу записываться, кто кому дарит
        #, для этого нужно вытащить из базы всех игроков в игре и бахнуть пачкой в функцию распределения
        #appoint_recipient(get_from_db_one_elem(game_name, "*", "player_list", "game_name")) <-- 
        #к этим данным нужен рейтинг каждого игрока допом.
        stage = stage_change(stage, game_name)
        data.pop(-1)
        data.append(stage) 
    elif stage == 1 and is_gave(game_name):
        stage = stage_change(stage, game_name)
        data.pop(-1)
        data.append(stage)
    elif stage == 2:
        #пересчёт рейтинга у того, кто дарил и смена состояния, но в 3 состоянии, если нет инфы об оценке, то писать, что её нет
        if get_from_db_one_elem(session['username'], "score", "player_list", "recipient_id", "-1"):
            stage = stage_change(stage, game_name)
            data.pop(-1)
            data.append(stage)
    elif stage == 3:
        print("Тяу")
        # Добавить в данные кому дарил, какую оценку поставил, кто дарил, какую оценку поставил (см Html)   
    player_list = get_from_db_one_elem(game_name, "*", "player_list", "game_name")
    players = []
    data.append(get_from_db_one_elem(get_from_db_one_elem(session['username'], "recipient_id", "player_list",
                                                          "player_id", "-1"), "login", "user", "id"))
    for i in range(len(player_list)):
        players.append(get_from_db_one_elem(player_list[i][2], "login", "user", "ID"))
    return flask.render_template('game.html', data=data, players=players)


@app.route('/set_score', methods=["GET", "POST"])
def set_score():
    game_name = get_from_db_one_elem(session['username'], "game_name", "player_list", "player_id", "-1")
    set_grades(session['username'], game_name, request.form['grade'])
    return game()


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    return flask.render_template('index.html')

# @app.route('discon')
