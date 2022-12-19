import socket
import threading
import sqlite3
import os
import re
import math
import dbase_API as db
import json
import time
import bash_scripts_exec as hdfs
from hashin_function import my_hash
import photo_recognizer
HEADER = 64
PORT = 2345
SERVER = "0.0.0.0"#socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
STATUS_LENGTH = 512
BUFF_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def use_CV_on_file(file:bytes, id1:int):
    db_conn = sqlite3.connect('Usrs.db')
    result = photo_recognizer.end_line(file)
    print(result)
    db.set_result(db_conn, id1, result)

def put_file(conn, login, db_conn):  # < target_dir < file < file_type < description < file_extension (if target_dir= / store in user dir else in user_dir/ target_dir)
    report = ""
    target_dir = recive_massage(conn).decode(FORMAT)
    file = recive_file(conn)
    #print(file)
    file_type = recive_massage(conn).decode(FORMAT) #тип файла: паспорт\снилс...
    #print(f"[+]file type{file_type}")
    description = recive_massage(conn).decode(FORMAT) #описание файла
    file_extension = recive_massage(conn).decode(FORMAT)
    #print(f"file extension {file_extension}")
    wd = db.work_directory(login, db_conn)
    if not wd:
        report += "[Erorre...]cant find user in DB while serching work_directory\n"
        send_status(conn, report)
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
    #print("[+]putting file in hdfs ....")
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

def send_list_to_confirm(conn, login:str, db_conn):
    data = db.select_not_confirm(db_conn, login)
    data = json.dumps(data)
    send(conn, data.encode("utf-8"))

def send_file_to_confirm(conn, login:str, db_conn):
    report = ""
    id1 = int(recive_massage(conn).decode(FORMAT))
    path, cv_result = db.get_file_path_by_id(db_conn, login, id1)
    if path == "not found":
        report += "can't find file path in a table"
        send_status(conn, report)
        return
    elif cv_result is None:
        report += "CV algoritm don't give result yet"
        send_status(conn, report)
        return
    else:
        report += "file path founded\n"
    r2, file = hdfs.get_file(path)
    print("[+]", path)
    report += r2
    if not file:
        send_status(conn, report)
        return
    else:
        send_status(conn, "success!")
    send_file(conn, file)
    time.sleep(1)
    send(conn, cv_result.encode("utf-8"))



def confirm_user_result(conn, login:str, db_conn):
    id1 = int(recive_massage(conn).decode(FORMAT))
    user_result = recive_massage(conn).decode(FORMAT)
    send_status(conn, str(db.confirm_result(db_conn, login, id1, user_result)))


def download_confirmed(conn, login:str, db_conn):
    send_file(conn, json.dumps(db.select_all_confirm(db_conn, login)).encode("utf-8"))



def check_pass(db_conn, login:str, password_hash:str) -> bool:
    return db.check_user(db_conn, login, password_hash)

def send_status(conn, status):
    msg = str(status).encode(FORMAT)
    msg += b' ' * (STATUS_LENGTH - len(msg))
    conn.send(msg)

def send(conn, message: bytes):
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)



def recive_massage(conn) -> str|None:
    msg_length = conn.recv(HEADER)
    #print("\n\n\n\n", msg_length)
    msg_length = msg_length.decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length)
        #print(msg_length)
        #print(len(msg))
        #print(msg)
        return msg.rstrip()
    return None



def send_file(conn, file:bytes):
    file_size = math.ceil(len(file) / 1024) * 1024
    file += b' ' * (file_size - len(file))
    send(conn, str(file_size).encode('utf-8'))
    for i in range(0, file_size, 1024):
        conn.send(file[i:i + 1024])


def recive_file(conn) -> bytes:
    #conn.blocking(True)
    file_size = int(recive_massage(conn).decode('utf-8'))
    file = b''
    while True:
        part = conn.recv(BUFF_SIZE)
        file += part
        if len(file) >= file_size:
            break
    print("recived_file")
    #print(file[:1024])
    #print()
    print(file[-1024:])
    return file.rstrip()



def handle_client(conn, addr):
    #conectected to db with userstry:
    DB_CONN = sqlite3.connect('Usrs.db')
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            login = recive_massage(conn).decode(FORMAT)
        except ConnectionResetError:
            conn.close()
            return
        except AttributeError :
            conn.close()
            return
        if login == DISCONNECT_MESSAGE:
            conn.close()
            print(f"[{addr}] DISCONECTED")
            return None
        try:
            password = my_hash(recive_massage(conn).decode(FORMAT))
        except ConnectionResetError:
            conn.close()
            return
        except AttributeError :
            conn.close()
            return
        if not check_pass(DB_CONN, login, password):
            send_status(conn, "[Errore]login not found")
        else:
            send_status(conn, "[+]login")
            break


    while True:
        try:
            msg = recive_massage(conn).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print(f"[{addr}] DISCONECTED")
                break
            elif msg == "put_file":
                put_file(conn, login, DB_CONN)
            elif msg == "get_list_for_cofirm":
                send_list_to_confirm(conn, login, DB_CONN)
            elif msg == "get_file_to_confirm":
                send_file_to_confirm(conn, login, DB_CONN)
            elif msg == "confirm":
                confirm_user_result(conn, login, DB_CONN)
            elif msg == "download_confirmed":
                download_confirmed(conn, login, DB_CONN)
            else:
                print(f"[ERRORE] command {msg} recived from {addr}: NOT FOUND")
            print(f"[{addr}] {msg}")
        except ConnectionResetError :
            conn.close()
            return
        except AttributeError :
            conn.close()
            return

        #send_status(conn, "Msg received")
    conn.close()



def create_tmp_dir():
    dir_temp_hdoop, _, _, _ = hdfs.get_vars()
    if not os.path.exists(dir_temp_hdoop):
        os.mkdir(dir_temp_hdoop)
    os.system(f"sudo chmod o+wr {dir_temp_hdoop}")

def start():
    server.bind(ADDR)
    os.system("sudo bash ./bash_scripts/start_hdfs.sh")
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
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")



if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()
