import pytest
import sqlite3
import sys
sys.path.append("..")
import add_user
CONN = sqlite3.connect("test.db")

import os
#start HDFS
os.system("sudo bash ./bash_scripts/start_hdfs.sh")
#creating_test_directory
os.system("sudo bash ./bash_scripts/mk_dir.sh /test")
os.system("sudo bash ./bash_scripts/mk_dir.sh /test/test")


@pytest.fixture(autouse=True)
def clear_db():
    print("Cleaning DB")
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS USERS(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login varchar(128),
            password_hash INTEGER, 
            work_directory varchar(128)
            );
        """)
    cursor.execute("""
    DELETE FROM USERS;
    """)
    conn.commit()


@pytest.fixture(autouse=True)
def mock_conn(monkeypatch):
    monkeypatch.setattr(sqlite3, "connect", lambda _: CONN)




#@pytest.mark.usefixtures("clear_db", "mock_conn")
@pytest.mark.parametrize("login, password, work_directory", [("test", "test", "/test/test")])
def test_add_user_normal_values(capsys, login, password, work_directory):
    add_user.add_user(login, password, work_directory)
    captured = capsys.readouterr()
    assert captured.out == f"user {login} added\n"

#@pytest.mark.usefixtures("clear_db", "mock_conn")
@pytest.mark.parametrize("login, password, work_directory", [("test", "test", "/test/test")])
def test_user_exist(capsys, login, password, work_directory):
    add_user.add_user(login, password, work_directory)
    captured = capsys.readouterr()
    assert captured.out == f"user {login} added\n"
    add_user.add_user(login, "password", "work_directory")
    captured = capsys.readouterr()
    assert captured.out == f"login '{login}' exists chose another\n"


@pytest.mark.parametrize("login, password, work_directory", [("", "test", "/test/test"),
                                                             ("test", "", "/test/test"),
                                                             ("test", "test", ""),
                                                             ("", "", "")])
def test_empty_data_exist(capsys, login, password, work_directory):
    add_user.add_user(login, password, work_directory)
    captured = capsys.readouterr()
    assert captured.out == "empty argument\n"


@pytest.mark.parametrize("login, password, work_directory", [("test", "test", "/test/not_existens"),
                                                             ("test", "test", "somthin_strange"),
                                                             ("test", "test", "/wtf/is_it")
                                                             ])
def test_non_existent_dir(capsys, login, password, work_directory):
    add_user.add_user(login, password, work_directory)
    captured = capsys.readouterr()
    assert captured.out == "directory not exist\n"
