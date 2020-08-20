import sqlite3

con = sqlite3.connect("login.db")
print("Creation successful")

con.execute("CREATE TABLE Users (user TEXT PRIMARY KEY, email TEXT NOT NULL, password TEXT NOT NULL)")
