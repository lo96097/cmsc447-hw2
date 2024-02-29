import sqlite3


def init():
    connection = sqlite3.connect('players.db')

    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    cur.execute("INSERT INTO players (name, id, score) VALUES (?, ?, ?)",
                ('Steve Smith', '211', '80')
                )

    cur.execute("INSERT INTO players (name, id, score) VALUES (?, ?, ?)",
                ('Jian Wong', '122', '92')
                )

    cur.execute("INSERT INTO players (name, id, score) VALUES (?, ?, ?)",
                ('Chris Peterson', '213', '91')
                )

    cur.execute("INSERT INTO players (name, id, score) VALUES (?, ?, ?)",
                ('Sai Patel', '524', '94')
                )

    cur.execute("INSERT INTO players (name, id, score) VALUES (?, ?, ?)",
                ('Andrew Whitehead', '425', '99')
                )

    cur.execute("INSERT INTO players (name, id, score) VALUES (?, ?, ?)",
                ('Lynn Roberts', '626', '90')
                )

    cur.execute("INSERT INTO players (name, id, score) VALUES (?, ?, ?)",
                ('Robert Sanders', '287', '75')
                )

    connection.commit()
    connection.close()
