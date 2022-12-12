import pytest
import sqlite3
import sys
from test_add_user import clear_db as clear_db_user
sys.path.append("..")
import dbase_API as script
import add_user
CONN = sqlite3.connect("test.db")
CONN2 = sqlite3.connect("test.db")
import os


@pytest.fixture(autouse=True)
def clear_db():
    print("Cleaning DB")
    conn = sqlite3.connect('test.db')
    script.crate_result_table_if_not_exists(conn)
    conn.cursor().execute("""
    DELETE FROM RESULT;
    """)
    conn.commit()


@pytest.fixture(autouse=True)
def mock_conn(monkeypatch):
    monkeypatch.setattr(sqlite3, "connect", lambda _: CONN)


def print_db(db1):
    crs = CONN.cursor()
    crs.execute(f"SELECT * FROM {db1}")
    print(crs.fetchall())
    

#@pytest.mark.usefixtures("clear_db", "mock_conn")
def test_alg_one():
    id1 = script.put_file_in_result_table(CONN, "login", "file_path", "file_type", "description"); assert len(script.select_not_confirm(CONN, "login")) == 1 and len(script.select_all_confirm(CONN, "login")) == 0
    
    script.set_result(CONN, id1, "result1"); assert len(script.select_not_confirm(CONN, "login")) == 1 and len(script.select_all_confirm(CONN, "login")) == 0

    script.confirm_results(CONN, id1, "result2");assert len(script.select_not_confirm(CONN, "login")) == 0 and len(script.select_all_confirm(CONN, "login")) == 1

    results = script.data_about_result(CONN, "login", "file_path"); assert results == (id1, "result2", "description")

    assert script.select_all_confirm(CONN, "login")[0] == ("file_path", "result2", "description")

    script.set_result(CONN, id1, "result3"); assert len(script.select_all_confirm(CONN, "login")) == 0


def test_alg_two():
    global CONN
    script.put_file_in_result_table(CONN, "login", "file_path", "file_type", None)
    with pytest.raises(Exception):
        id1 = script.put_file_in_result_table(CONN, "login", "file_path", None, None)

    with pytest.raises(Exception):
        id1 = script.put_file_in_result_table(CONN, "login", None, "dsd", None)

    with pytest.raises(Exception):
        id1 = script.put_file_in_result_table(CONN, None, "sd", "dsd", None)
    CONN = CONN2


@pytest.mark.usefixtures("clear_db_user", "mock_conn")
def test_alg_three():
    script.crate_user_table_if_not_exists(CONN)
    add_user.add_user("login", "password_hash", "/test")
    print_db("USERS")
    assert script.work_directory("login", CONN) ==  "/test"
    assert script.check_login_exist("login", CONN.cursor())
