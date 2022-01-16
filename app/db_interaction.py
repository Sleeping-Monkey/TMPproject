import sqlite3


def add_user(login, passwd):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """INSERT INTO User (Login, Password) VALUES (?, ?)"""
    data = (login, passwd)
    curs.execute(sql_req, data)
    conn.commit()
    conn.close()


def log_user(login, passwd):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """SELECT Password FROM User WHERE Login = ?"""
    data = (login,)
    passwd_check = (curs.execute(sql_req, data)).fetchall()
    conn.close()
    if passwd == passwd_check[0][0]:
        return True
    else:
        return False


def create_game(game_name, player_limit, creator_name):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """INSERT INTO game_info (game_name, creator_id, player_limit) VALUES (?,?,?)"""
    data = (game_name, id_by_name(creator_name), player_limit)
    curs.execute(sql_req, data)
    conn.commit()
    conn.close()


def connect_game(game_name, name):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """INSERT INTO player_list (game_name, player_id) VALUES (?,?)"""
    data = (game_name, id_by_name(name))
    curs.execute(sql_req, data)
    conn.commit()
    conn.close()


def id_by_name(name):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """SELECT ID FROM User WHERE login = ?"""
    data = (name,)
    id = (curs.execute(sql_req, data)).fetchall()
    conn.close()
    return id[0][0]

