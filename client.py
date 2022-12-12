import socket

HEADER = 64
PORT = 2345
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
STATUS_LENGTH = 512

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def autarisation(login, password):
    send(login.encode(FORMAT))
    send(password.encode(FORMAT))

def put_file(file_path: str, target_dir: str, file_type: str, description: str, file_extension: str) -> None:
    send("put_file".encode(FORMAT))
    send(target_dir.encode(FORMAT))
    with open(file_path, 'br') as f:
        send(f.read())
    send(file_type.encode(FORMAT))
    send(description.encode(FORMAT))
    send(file_extension.encode(FORMAT))
    return recive_status_answer()

def send(message: bytes):
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def recive_status_answer() -> str:
    return client.recv(STATUS_LENGTH).decode(FORMAT)


def setup():
    autarisation("admin", "admin")

setup()
a = put_file("1.txt", "", "some_type", "testing data", ".txt")
print(a)
send(DISCONNECT_MESSAGE.encode(FORMAT))
