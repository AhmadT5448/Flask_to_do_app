import sqlite3

conn = sqlite3.connect('to_do_list.sqlite')

cursor = conn.cursor()

sql_query = """ CREATE TABLE to_do_list (
    sr integer PRIMARY KEY,
    to_do text NOT NULL 
)"""


cursor.execute(sql_query)
