import pytest
import sys
sys.path.append("..")
import socket_djarvis_server as script
import add_user
import dbase_API as db
import client as client
import bash_scripts_exec as hdfs
import sqlite3
import os
from hashin_function import my_hash
CONN = sqlite3.connect("Usrs.db")
db.crate_user_table_if_not_exists(CONN)
db.crate_result_table_if_not_exists(CONN)

#start HDFS
os.system("sudo bash ./bash_scripts/start_hdfs.sh")
import threading
t = threading.Thread(target=script.start)
t.daemon = True
t.start()
import time
time.sleep(5)
client.set_up()


@pytest.fixture(autouse=True)
def clear_hdfs_and_SQL():
    #creating and clear test directory
    rep, _ = hdfs.mk_dir("/test")
    print(rep)
    rep, _ = hdfs.mk_dir("/test/test")
    print(rep)
    rep, _ = hdfs.clear_dir("/test/test")
    print(rep)
    CONN.cursor().execute("DELETE FROM USERS WHERE login=?", ("test",))
    CONN.cursor().execute("DELETE FROM RESULT WHERE login=?", ("test",))
    CONN.commit()
    add_user.add_user("test", my_hash("test"), "/test")

def test_unsuccess_login():
    a = client.autarisation("jksadfkljgaljoaijgojivjl;akjsfljqetest", "test")
    assert not a
    a = client.autarisation("test", "test111")
    assert not a

def test_put_file_success():
    os.system(f'touch ./test/1.txt; echo "test data" > ./test/1.txt')
    #os.system(f"sudo bash ./bash_scripts/put_file.sh ./test/1.txt /test/test")
    a = client.autarisation("test", "test")
    assert a
    a = client.put_file("./test/1.txt", "/test", "some_type", "testing data", ".txt")
    assert "success!" in a
    rep, ls_list = hdfs.ls_dir("/test/test")
    print(rep)
    assert "/test/test/test_0.txt" in ls_list['files'] and len(ls_list['files']) == 1
    #client.send(client.DISCONNECT_MESSAGE.encode(client.FORMAT))
    #client.autarisation("test", "test")
    a = client.put_file("./test/1.txt", "/test", "some_type", "testing data", ".txt")
    assert "success!" in a
    rep, ls_list = hdfs.ls_dir("/test/test")
    print(rep)
    assert "/test/test/test_2.txt" in ls_list['files'] and len(ls_list['files']) == 2

def test_get_list_to_confirm():
    os.system(f'touch ./test/1.txt; echo "test data" > ./test/1.txt')
    a = client.put_file("./test/1.txt", "/test", "some_type", "testing data", ".txt")
    assert "success!" in a
    a = client.get_list_for_cofirm()
    assert len(a) == 1
    assert a[0][1] == "/test/test/test_0.txt" and a[0][2] == "testing data"
    a = client.put_file("./test/1.txt", "/test", "some_type", "testing data", ".txt")
    assert "success!" in a
    a = client.get_list_for_cofirm()
    assert len(a) == 2


def test_get_file_to_confirm():
    os.system(f'touch ./test/1.txt; echo "test data" > ./test/1.txt')
    a = client.put_file("./test/1.txt", "/test", "some_type", "testing data", ".txt")
    assert "success!" in a
    a = client.get_list_for_cofirm()
    assert len(a) == 1
    id1 = a[0][0]
    a = client.get_file_to_confirm(id1)
    assert a[0] is None # алгоритм не закончил работу поэтому оно вернет None
    time.sleep(10)
    a = client.get_file_to_confirm(id1)
    file = a[0]
    assert file == b"test data"

def test_confirm_result():
    os.system(f'touch ./test/1.txt; echo "test data" > ./test/1.txt')
    a = client.put_file("./test/1.txt", "/test", "some_type", "testing data", ".txt")
    assert "success!" in a
    a = client.get_list_for_cofirm()
    assert len(a) == 1
    id1 = a[0][0]
    a = client.confirm_result(id1, "user_result")
    assert a == 1
    a = client.get_list_for_cofirm()
    assert len(a) == 0

def test_download_confirmed():
    os.system(f'touch ./test/1.txt; echo "test data" > ./test/1.txt')
    a = client.put_file("./test/1.txt", "/test", "some_type", "testing data", ".txt")
    assert "success!" in a
    import time 
    time.sleep(10)
    a = client.get_list_for_cofirm()
    assert len(a) == 1
    id1 = a[0][0]
    a = client.confirm_result(id1, "user_result")
    assert a == 1
    a = client.download_confirmed()
    assert len(a) == 1
    assert tuple(a[0]) == ("/test/test/test_0.txt", 'user_result', "testing data")



    
def test_clenup():
    CONN.cursor().execute("DELETE FROM USERS WHERE login=?", ("test",))
    CONN.cursor().execute("DELETE FROM RESULT WHERE login=?", ("test",))
    CONN.commit()
    # client.send(client.DISCONNECT_MESSAGE.encode(client.FORMAT))
    print("all tasts done press ctrl + C to stap server")

