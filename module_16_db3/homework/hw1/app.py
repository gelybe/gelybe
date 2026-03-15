import sqlite3

with open('create_schema.sql', 'r') as f:
    sql_script = f.read()

with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()