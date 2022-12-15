import sqlite3
import subprocess
from typing import Tuple
from hashin_function import my_hash

def crate_user_table_if_not_exists(CONN):
    curs = CONN.cursor()
    curs.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login varchar(128),
                password_hash varchar(512),
                work_directory varchar(128)
                );
    """)
    CONN.commit()


def crate_result_table_if_not_exists(CONN):
    curs = CONN.cursor()
    curs.execute("""
            CREATE TABLE IF NOT EXISTS RESULT (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login varchar(128) NOT NULL,
                file_full_name varchar(128) NOT NULL,
                result varchar(1024) ,
                file_type varchar(128) NOT NULL,
                confirm BOOLEAN CHECK (confirm IN (0, 1) ),
                description varchar(128)
                );
    """)
    CONN.commit()


def work_directory(login: str, CONN) -> str:
        cursor = CONN.cursor()
        cursor.execute("""
                        SELECT work_directory
                        FROM USERS
                        WHERE login = ?
                   """, (login,))
        try:
            return cursor.fetchone()[0]
        except TypeError:
            return None

def put_file_in_result_table(CONN, login: str, file_path: str, file_type: str, description) -> int:#login - user login that storage file file_path - full file path from root to file file_type - type of document: passport\snils\...
    curs = CONN.cursor()
    curs.execute("""
            INSERT INTO RESULT (login, file_full_name, file_type, confirm, description)
            VALUES(?, ?, ?, 0, ?)
            """, (login, file_path, file_type, description))
    CONN.commit()
    return curs.lastrowid


def confirm_result(CONN, login:str, id1: int, result: str) -> int: #return count modifited rows||set result from client
    curs = CONN.cursor()
    curs.execute("""
            UPDATE RESULT 
            SET confirm = 1,
                result = ?
            WHERE id = ? AND login = ?
            """, (result, id1, login))
    CONN.commit()
    return curs.rowcount


def set_result(CONN, id1: int, result: str):  #set result = result of CV
    curs = CONN.cursor()
    curs.execute("""
            UPDATE RESULT 
            SET confirm = 0,
                result = ?
            WHERE id = ?
            """, (result, id1))
    CONN.commit()


def data_about_result(CONN, login: str, file_path: str) -> Tuple[int, str, str]: #return (id, result, description)
    cursor = CONN.cursor()
    cursor.execute("""
                        SELECT id,
                               result,
                               description
                        FROM RESULT
                        WHERE login = ? AND file_full_name = ?
                   """, (login, file_path))
    return cursor.fetchone()


def get_file_path_by_id(CONN, login:str, id1:str) -> Tuple[str, str]:
    cursor = CONN.cursor()
    cursor.execute("""
                        SELECT file_full_name,
                            result
                        FROM RESULT
                        WHERE login = ? AND id = ?
                   """, (login, id1))
    try:
        data = cursor.fetchone()
        print(data)
        return (data[0], data[1])
    except TypeError:
        return ("not found", "not found")


def select_not_confirm(CONN, login: str) -> Tuple[Tuple[int, str, str]]: # return list of tuples with id and file path that aren't confirmed
    cursor = CONN.cursor()
    cursor.execute("""
                    SELECT id,
                           file_full_name,
                           description
                    FROM RESULT 
                    WHERE login = ? AND confirm = 0
                """, (login, ))
    return cursor.fetchall()


def select_all_confirm(CONN, login: str) -> Tuple[Tuple[str, str, str]]: # return list of tuples with id and file path that aren't confirmed
    cursor = CONN.cursor()
    cursor.execute("""
                    SELECT file_full_name,
                           result,
                           file_type,
                           description
                    FROM RESULT 
                    WHERE login = ? AND confirm = 1
                """, (login, ))
    return cursor.fetchall()


def check_login_exist(login: str, curs) -> bool:
    curs.execute('''
                      SELECT * from Users
                      WHERE login = ?
                  ''', (login, ))
    return bool(curs.fetchone())


def check_user(CONN, login:str, password_hash:str) -> bool:
    cursor = CONN.cursor()
    #print((login, password_hash), "+++++++++++++++++++++++++++++++++++++")
    cursor.execute("""
                    SELECT * 
                    FROM USERS
                    WHERE login = ? and password_hash = ?
                """, (login, password_hash))
    a = cursor.fetchall()
    #print(a)
    return len(a) > 0
