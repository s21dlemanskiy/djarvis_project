import sqlite3
CONN = sqlite3.connect("Usrs.db")
cursor=CONN.cursor()
cursor.execute("SELECT * FROM USERS")
print("Usres:", cursor.fetchall())
cursor.execute("SELECT * FROM RESULT")
print("Results:", cursor.fetchall())
