import socket
import json
from typing import Tuple, Any
HEADER = 64
PORT = 2345
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "0.0.0.0"
STATUS_LENGTH = 512

client = None
def set_up():
    global client
    ADDR = (SERVER, PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("client connected")

def autarisation(login, password) -> bool:
    send(login.encode(FORMAT))
    send(password.encode(FORMAT))
    answer = recive_status_answer()
    if "[+]login" not in answer:
        print(answer)
        return False
    else:
        return True


def get_list_for_cofirm() -> Tuple[Tuple[str, str]]:
    send("get_list_for_cofirm".encode(FORMAT))
    data = json.loads(recive_massage().decode("utf-8"))
    return data

def get_file_to_confirm(id1: int) -> Tuple[None|bytes, None|str]:
    send("get_file_to_confirm".encode(FORMAT))
    send(str(id1).encode(FORMAT))
    answer = recive_status_answer()
    if not "success!" in answer:
        print("[+]", answer)
        return (None, None)
    file = recive_massage()
    cv_result = recive_massage().decode('utf-8')
    return (file, cv_result)


def confirm_result(id1:int, user_result:str) -> int: #return count modifiter rows
    send("confirm".encode(FORMAT))
    send(str(id1).encode("utf-8"))
    send(user_result.encode("utf-8"))
    return int(recive_status_answer())


def download_confirmed() -> Tuple[Tuple[Any]]:
    send("download_confirmed".encode(FORMAT))
    result = json.loads(recive_massage().decode("utf-8"))
    return result




def put_file(file_path: str, target_dir: str, file_type: str, description: str, file_extension: str) -> str:
    send("put_file".encode(FORMAT))
    send(target_dir.encode(FORMAT))
    with open(file_path, 'br') as f:
        send(f.read())
    send(file_type.encode(FORMAT))
    send(description.encode(FORMAT))
    send(file_extension.encode(FORMAT))
    return recive_status_answer()


def recive_massage() -> str|None:
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length)
        return msg.rstrip()
    return None




def send(message: bytes):
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def recive_status_answer() -> str:
    return client.recv(STATUS_LENGTH).decode(FORMAT)

if __name__ == "__main__":
    set_up()
    autarisation("test", "test2")
    autarisation("test", "test")
    print(put_file("./test/1.txt", "test", "smth", "smth else", ".txt"))
    a = get_list_for_cofirm()
    print(a)
    id1 = a[0][0]
    a = get_file_to_confirm(id1)
    print(a)
    a =  confirm_result(id1, "user_result")
    print("edited:", a)
    print(download_confirmed())
    send(DISCONNECT_MESSAGE.encode("utf-8"))
