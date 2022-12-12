import socket 
import threading
import sqlite3
import os
import re
import dbase_API as db
import bash_scripts_exec as hdfs 
HEADER = 64
PORT = 2345
SERVER = "0.0.0.0"#socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
STATUS_LENGTH = 512

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def use_CV_on_file(file:bytes, id1:int): 
    db_conn = sqlite3.connect('Usrs.db')
    print("типо юзаем алгоритмы МЛ")
    import time
    time.sleep(5)
    db.set_result(db_conn, id1, "CV_result")

def put_file(conn, login, db_conn):  # < target_dir < file < file_type < description < file_extension (if target_dir= / store in user dir else in user_dir/ target_dir)
    report = ""
    target_dir = recive_massage(conn).decode(FORMAT)
    file = recive_massage(conn)
    file_type = recive_massage(conn).decode(FORMAT) #тип файла: паспорт\снилс...
    description = recive_massage(conn).decode(FORMAT) #описание файла
    file_extension = recive_massage(conn).decode(FORMAT)
    wd = db.work_directory(login, db_conn)
    if not wd:
        report += "[Erorre...]cant find user in DB while serching work_directory\n"
        send_status(report)
        return 
    while len(target_dir) > 0 and target_dir[0] == "/": 
        target_dir = target_dir[1:]
    target_dir = os.path.join(wd, target_dir)
    r, ls_result = hdfs.ls_dir(target_dir)
    report += r
    if ls_result is None:
        send_status(conn, report)
        return
    if len(ls_result["files"]) == 0:
        name = f"{login}_0"
    else:
        num = len(ls_result["files"])
        #num = 0
        #for file_name in ls_result["files"]:
        #    string = re.search(login + r"_\d+.?\w+$", file_name).group()
        #    string = re.search("^"login + r"_\d+", string).group()
        #    string = re.search(r"\d+", string).group()
        #    if string:
        #        num = max(num, string)
        name = f"{login}_{num + 1}"
    name += file_extension
    r, status = hdfs.put_file(file, name, target_dir)
    report += r
    if not status:
        send_status(conn, report)
        return
    full_file_path = os.path.join(target_dir, name)
    id1 = db.put_file_in_result_table(db_conn, login, full_file_path, file_type, description)
    send_status(conn, "success!")
    thread = threading.Thread(target=use_CV_on_file, args=(file, id1))
    thread.start()



def check_pass(login, password_hash):
    if login == "admin" and password_hash == hash("admin"):
        return True
    else:
        return False


def send_status(conn, status):
    msg = str(status).encode(FORMAT)
    msg += b' ' * (STATUS_LENGTH - len(msg))
    conn.send(msg)


def recive_massage(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length)
        return msg.rstrip()
    return None

def handle_client(conn, addr):
    #conectected to db with users 
    DB_CONN = sqlite3.connect('Usrs.db')

    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    login = recive_massage(conn).decode(FORMAT)
    password = hash(recive_massage(conn).decode(FORMAT))
    if not check_pass(login, password):
        conn.close()
        return None
    while connected:
        msg = recive_massage(conn).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
        elif msg == "put_file":
            put_file(conn, login, DB_CONN)
        elif msg == "get_file":
            put_file(conn, login, DB_CONN)
        else:
            print(f"[ERRORE] command {msg} recived from {addr}: NOT FOUND")
        print(f"[{addr}] {msg}")
        send_status(conn, "Msg received")
    conn.close()



def create_tmp_dir():
    dir_temp_hdoop, _, _, _ = hdfs.get_vars()
    if not os.path.exists(dir_temp_hdoop):
        os.mkdir(dir_temp_hdoop)


def start():
    create_tmp_dir()
    DB_CONN = sqlite3.connect('Usrs.db')
    db.crate_user_table_if_not_exists(DB_CONN)
    db.crate_result_table_if_not_exists(DB_CONN)
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")



if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()
