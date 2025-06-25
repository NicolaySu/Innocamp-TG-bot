import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    state BOOLEAN,
    resum TEXT
)
''')


async def set_param(param, value):
    cur.execute(f"INSERT INTO users ({param}) VALUES (?)", (value,))
    con.commit()


async def upd_param(exec_param, where_param, value, where_param_is):
    cur.execute(f'UPDATE Users SET {exec_param} = ? WHERE {where_param} = ?', (value, where_param_is))
    con.commit()
