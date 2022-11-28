import socket 
import threading

HEADER = 64
PORT = 2345
SERVER = "0.0.0.0"#socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
STATUS_LENGTH = 512


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def put_file(conn, login):
    print("putting command not done")

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
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg.rstrip()
    return None

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    login = recive_massage(conn)
    password = hash(recive_massage(conn))
    if not check_pass(login, password):
        conn.close()
        return None
    while connected:
        msg = recive_massage(conn)
        if msg == DISCONNECT_MESSAGE:
            connected = False
        elif msg == "put_file":
            put_file(conn, login)
        else:
            print(f"[ERRORE] command {msg} recived from {addr}: NOT FOUND")
        print(f"[{addr}] {msg}")
        send_status(conn, "Msg received")
    conn.close()
                                                                                                                                    
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")



print("[STARTING] server is starting...")
start()
