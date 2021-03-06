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
from app.db_interaction import update_mmr
from app.db_interaction import if_all_scored
import random


from sys import stderr

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
                games = get_from_db_one_elem(session['username'], "*", "player_list", "player_id", "-1")
                data = []
                rating = get_from_db_one_elem(session['username'], "mmr", "user", "login")
                for i in range(len(games)):
                    data.append(games[i][1])
                return flask.render_template('user.html', data=data, rating=rating)
        except KeyError:
            return "Please log in"
    elif request.method == "POST":
        login, passwd = request.form['name'], request.form['password']
        if log_user(login, passwd):
            session["username"] = login
            games = get_from_db_one_elem(session['username'], "*", "player_list", "player_id", "-1")
            data = []
            rating = get_from_db_one_elem(session['username'], "mmr", "user", "login")
            for i in range(len(games)):
                data.append(games[i][1])
            return flask.render_template('user.html', data=data, rating=rating)
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
    data = []
    games = get_from_db_one_elem(session['username'], "*", "player_list", "player_id", "-1")
    rating = get_from_db_one_elem(session['username'], "mmr", "user", "login")
    for i in range(len(games)):
        data.append(games[i][1])
    return flask.render_template('user.html', data=data, rating=rating)


@app.route('/game', methods=["GET", "POST"])
def game():
    gm_nm = ""
    results = [-1, -1, -1, -1]
    if request.method == "POST":
        game_name = request.form['gameid']
    else:
        game_name = get_from_db_one_elem(session['username'], "game_name", "player_list", "player_id", "-1")
    if not connected(session['username'], game_name):
        try:
            if is_space_to_connect(game_name):
                connect_game(game_name, session['username'])
            else:
                data = 0
                rating = get_from_db_one_elem(session['username'], "mmr", "user", "login")
                return flask.render_template('user.html', data=data, rating=rating)
        except TypeError:
            data = []
            games = get_from_db_one_elem(session['username'], "*", "player_list", "player_id", "-1")
            for i in range(len(games)):
                data.append(games[i][1])
            data.append(0)
            rating = get_from_db_one_elem(session['username'], "mmr", "user", "login")
            return flask.render_template('user.html', data=data, rating=rating)
    if request.args.get("a") == "1":
        pr_gave(session['username'], game_name)
    stage = get_from_db_one_elem(game_name, "stage", "game_info", "game_name")
    data = [game_name, stage]
    if request.method == "POST":
        gm_nm = request.form["gameid"]
        data = [gm_nm, get_from_db_one_elem(gm_nm, "stage", "game_info", "game_name")]

    if stage == 0 and not is_space_to_connect(game_name):
        presents(game_name)
        # write_to_bd(l_ist)
        #??????, ?????????? ?????????? ??????????????????, ???????????? ?? ???????? ????????????????????????, ?????? ???????? ??????????
        #, ?????? ?????????? ?????????? ???????????????? ???? ???????? ???????? ?????????????? ?? ???????? ?? ?????????????? ???????????? ?? ?????????????? ??????????????????????????
        appoint_recipient(get_from_db_one_elem(game_name, "*", "player_list", "game_name"))
        stage = stage_change(stage, game_name)
        data.pop(-1)
        data.append(stage)
    elif stage == 1 and is_gave(game_name):
        stage = stage_change(stage, game_name)
        data.pop(-1)
        data.append(stage)
    elif stage == 2:
        if if_all_scored(game_name) != -1:
            if get_from_db_one_elem(session['username'], "score", "player_list", "recipient_id", "-1"):
                stage = stage_change(stage, game_name)
                data.pop(-1)
                data.append(stage)

    if stage == 3:
        update_mmr(session['username'])
        results[0] = get_from_db_one_elem(get_from_db_one_elem(session['username'], "player_id",
                                                               "player_list", "recipient_id", "-1"), "login", "User",
                                          "ID")
        results[1] = get_from_db_one_elem(session['username'], "score", "player_list", "recipient_id", "-1")
        results[2] = get_from_db_one_elem(get_from_db_one_elem(session['username'], "recipient_id",
                                                               "player_list", "player_id", "-1"), "login", "User", "ID")
        results[3] = get_from_db_one_elem(session['username'], "score", "player_list", "player_id", "-1")
        if results[3] == -1:
            results[3] = "?????? ?????????????? ???????? ???? ????????????"
    if gm_nm != "":
        player_list = get_from_db_one_elem(gm_nm, "*", "player_list", "game_name")
    else:
        player_list = get_from_db_one_elem(game_name, "*", "player_list", "game_name")
    players = []
    data.append(get_from_db_one_elem(get_from_db_one_elem(session['username'], "recipient_id", "player_list",
                                                          "player_id", "-1"), "login", "user", "id"))
    is_scored = get_from_db_one_elem(session['username'], "score", "player_list", "recipient_id", "-1")
    for i in range(len(player_list)):
        players.append(get_from_db_one_elem(player_list[i][2], "login", "user", "ID"))
    return flask.render_template('game.html', data=data, players=players, results=results, is_scored=is_scored)


@app.route('/set_score', methods=["GET", "POST"])
def set_score():
    if request.method == "GET":
        update_mmr(session['username'])
    stage = 2
    results = [-1, -1, -1, -1]
    game_name = get_from_db_one_elem(session['username'], "game_name", "player_list", "player_id", "-1")
    if request.method == "POST":
        set_grades(session['username'], game_name, request.form['grade'])

    results[0] = get_from_db_one_elem(get_from_db_one_elem(session['username'], "player_id",
                                                           "player_list", "recipient_id", "-1"), "login", "User", "ID")
    results[1] = get_from_db_one_elem(session['username'], "score", "player_list", "recipient_id", "-1")
    results[2] = get_from_db_one_elem(get_from_db_one_elem(session['username'], "recipient_id",
                                                           "player_list", "player_id", "-1"), "login", "User", "ID")
    results[3] = get_from_db_one_elem(session['username'], "score", "player_list", "player_id", "-1")
    if results[3] == -1:
        results[3] = "?????? ?????????????? ???????? ???? ????????????"
    if request.method == "POST":
        update_mmr(session['username'])
        if if_all_scored(game_name) != -1:
            stage = get_from_db_one_elem(game_name, "stage", "game_info", "game_name")
            if stage != 3:
                stage = stage_change(stage, game_name)
    data = (game_name, stage)
    is_scored = get_from_db_one_elem(session['username'], "score", "player_list", "recipient_id", "-1")
    return flask.render_template('game.html', data=data, results=results, is_scored=is_scored)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    return flask.render_template('index.html')

