import sqlite3

conn = sqlite3.connect('2048.db')

with conn:
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS fenbiao(
       id INTEGER PRIMARY KEY,
       gaofen INT);
    ''')

    cur.execute('INSERT INTO fenbiao(gaofen) VALUES(?);', [0])
    conn.commit()
