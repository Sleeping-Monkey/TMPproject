import sqlite3

from sys import stderr
import random

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
    #print("!!!DATA!!!", file=stderr)
    #print(data, file=stderr)
    #print("!!!DATA!!!", file=stderr)
    if what_to_return != "*" and data != []:
        return data[0][0]
    else:
        return data


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


def stage_change(stage, game_name):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """UPDATE game_info set stage = ? WHERE game_name = ?"""
    data = (stage+1, game_name)
    curs.execute(sql_req, data)
    conn.commit()
    conn.close()
    return stage+1


def is_gave(game_name):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """SELECT MIN(is_give) FROM player_list WHERE game_name = ?"""
    data = (game_name,)
    data = (curs.execute(sql_req, data)).fetchall()
    conn.close()
    return data[0][0]


def pr_gave(player, game_name):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """UPDATE player_list set is_give = 1 WHERE player_id = ? and game_name = ?"""
    data = (get_from_db_one_elem(player), game_name,)
    curs.execute(sql_req, data)
    conn.commit()
    conn.close()


def set_grades(player, game_name, grade):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """UPDATE player_list set score = ? WHERE recipient_id = ? and game_name = ?"""
    data = (grade, get_from_db_one_elem(player), game_name,)
    curs.execute(sql_req, data)
    conn.commit()
    conn.close()


def presents(game_name="bebra"):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    sql_req = """SELECT User.ID, User.Mmr
        FROM player_list JOIN User ON User.ID == player_list.player_id AND player_list.game_name == ?"""
    data = (game_name,)
    data = (curs.execute(sql_req, data)).fetchall()
    conn.close()
    if len(data) == 1:
        write_to_bd([data[0][0], data[0][0]], game_name) # Заглушка моя, но вообще таких ебланов надо банить 
        return
    result = [] # [кому]
    id_data = []
    for i in range(len(data)):
        id_data.append(i)
    counter = 0
    best_dist = -1
    while counter < len(id_data) // 2:
        random.shuffle(id_data)
        dist = 0
        flag = 1
        for i in range(len(data)):
            if data[id_data[i]][0] == data[i][0]:
                flag = 0
                break
            elif data[id_data[i]][1] > data[i][1]:
                dist += int(data[id_data[i]][1]) - int(data[i][1])
            else:
                dist += int(data[i][1]) - int(data[id_data[i]][1])
        if flag == 1:
            counter += 1
            if best_dist == -1 or best_dist > dist:
                best_dist = dist
                result = id_data
    for i in range(len(data)):
        write_to_bd([data[result[i]][0], data[i][0]], game_name)
    # print(data)
#     return data


def write_to_bd(data, game_name):
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    for i in data:
        sql_req = """UPDATE player_list set recipient_id = ? WHERE player_id = ? and game_name = ?"""
        req = (data[0], data[1],game_name)
        curs.execute(sql_req, req)
        conn.commit()
    conn.close()


