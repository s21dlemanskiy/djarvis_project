import sqlite3

CONN = sqlite3.connect('Usrs.db')

curs = CONN.cursor()
curs.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login varchar(128),
                password_hash INTEGER,
                work_directory varchar(128)
                );
""")


def add_uesr(login: str, password_hash:int, work_directory:str):
    cursor.execute('''
                      SELECT * from Users
                      WHERE login = ?
                  ''', (login, ))
    if bool(cursor.fetchone()):
        print(f"login '{login}' exists chose another")
        return
    test = subprocess.check_output(f"sudo bash ./bash_scripts/test_dir_file.sh {work_directory}")
    if test == "not exist":
        print("directory not exist")
        return
    elif test == "exist":
        curs.execute("""
                INSERT INTO USERS(login, password_hash, work_directory)
                VALUES(?, ?, ?)
                """, (login, password_hash, work_directory))
        CONN.commit()
        print(f"user {login} added"
        return
    else:
        print(f"unexpected answer from bash script:{test}"
        return


login = input("login:")
print()
password_hash = hash(input("password:"))
print()
working_directory = input("working_directory")
add_user(login, password_hash, work_directory)
