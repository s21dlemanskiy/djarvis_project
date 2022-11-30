import sqlite3
import subprocess

def crate_table_if_not_exists(curs):
    curs.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login varchar(128),
                password_hash INTEGER,
                work_directory varchar(128)
                );
    """)



def check_login_exist(login: str, curs) -> bool:
    curs.execute('''
                      SELECT * from Users
                      WHERE login = ?
                  ''', (login, ))
    return bool(curs.fetchone())

def add_user(login: str, password_hash:int, work_directory:str) -> None:
    if not login or not password_hash or not work_directory:
        print("empty argument")
        return 


    CONN = sqlite3.connect('Usrs.db')
    curs = CONN.cursor()
    crate_table_if_not_exists(curs)
    
    login_exist = check_login_exist(login, curs)
    if login_exist:
        print(f"login '{login}' exists chose another")
        return
    test = subprocess.check_output(f"sudo bash ./bash_scripts/test_dir_file.sh {work_directory}", shell=True)
    if test == b"not exist\n":
        print("directory not exist")
        return 
    elif test == b"exist\n":
        curs.execute("""
                INSERT INTO USERS(login, password_hash, work_directory)
                VALUES(?, ?, ?)
                """, (login, password_hash, work_directory))
        CONN.commit()
        print(f"user {login} added")
        return 
    else:
        print(f"unexpected answer from bash script:{test}")
        return 

def start():
    login = input("login:")
    password_hash = hash(input("password:"))
    work_directory = input("working_directory")
    add_user(login, password_hash, work_directory)

if __name__ == "__main__":
    start()
