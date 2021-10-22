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
