import sqlite3


def add_user(login, passwd):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """INSERT INTO User (Login, Password, Mmr) VALUES (?, ?, ?)"""
    data = (login, passwd, 1000)
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
    data = (game_name, get_from_db_one_elem(creator_name), player_limit)
    curs.execute(sql_req, data)
    conn.commit()
    conn.close()


def connect_game(game_name, name):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """INSERT INTO player_list (game_name, player_id) VALUES (?,?)"""
    data = (game_name, get_from_db_one_elem(name),)
    curs.execute(sql_req, data)
    conn.commit()
    conn.close()


# def id_by_name(name):
#     conn = sqlite3.connect("database.db")
#     curs = conn.cursor()
#     what_to_return = "ID"
#     table_name = "User"
#     column = "login"
#     sql_req = """SELECT """ + what_to_return + """ FROM """ + table_name + """ WHERE """ + column + """ = ?"""
#     data = (name,)
#     id = (curs.execute(sql_req, data)).fetchall()
#     conn.close()
#     return id[0][0]


def get_from_db_one_elem(search_by_what, what_to_return="ID", table_name="User", column="login", a="0"):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """SELECT """ + what_to_return + """ FROM """ + table_name + """ WHERE """ + column + """ = ?"""
    data = (search_by_what,)
    if a == "-1":
        name = get_from_db_one_elem(search_by_what)
        data = (name,)
    data = (curs.execute(sql_req, data)).fetchall()
    conn.close()
    return data[0][0]


def is_space_to_connect(game_name):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """SELECT COUNT(player_id) FROM player_list WHERE game_name = ?"""
    data = (game_name,)
    data = (curs.execute(sql_req, data)).fetchall()
    lim = get_from_db_one_elem(game_name, "player_limit", "game_info", "game_name")
    conn.close()
    return lim-data[0][0]


def connected(player_id, game_name):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """SELECT * FROM player_list WHERE game_name = ? AND player_id = ?"""
    data = (game_name, get_from_db_one_elem(player_id),)
    if ((curs.execute(sql_req, data)).fetchone()) is None:
        return 0
    else:
        return 1


def presents(game_name="bebra"):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """SELECT User.ID, User.Mmr
        FROM player_list JOIN User ON User.ID == player_list.player_id AND player_list.game_name == ?"""
    data = (game_name,)
    data = (curs.execute(sql_req, data)).fetchall()
    conn.close()
    # print(data)
#     return data




