#!/usr/bin/env python

import sqlite3
import flask
import init_db

APP = flask.Flask(__name__)

headings = ("Name", "ID", "Score")

def get_db_connection():
	conn = sqlite3.connect('players.db')
	conn.row_factory = sqlite3.Row
	return conn
	
	
@APP.route('/')

def index():
	conn = get_db_connection()
	rows = conn.execute('SELECT * FROM players').fetchall()
	conn.close()
	return flask.render_template('index.html', headings=headings, players = rows)
 
@APP.route('/addplayer', methods=('GET','POST'))

def addplayer():
	if flask.request.method == 'POST':
		name = flask.request.form['name']
		id = flask.request.form['id']
		score = flask.request.form['score']
     
		with sqlite3.connect('players.db') as players:
			cursor = players.cursor()
			cursor.execute("INSERT INTO players (name,id,score) VALUES (?,?,?)",(name, id, score))
			players.commit()
		return index()
	else:
		return flask.render_template('/addplayer.html')

@APP.route('/<int:i>/delete', methods=('POST',))

def delete(i):
	conn = get_db_connection()
	check=conn.execute('SELECT * FROM players WHERE i = ?',(i,))
	if check is None:
		abort(404, f"Player not found.")
	else:	
	        conn.execute('DELETE FROM players WHERE i = ?',(i,))
	        conn.commit()
	        return index()
	
	
	
@APP.route('/<int:i>/update', methods=('GET','POST',))

def update(i):
	if flask.request.method == 'POST':
		name = flask.request.form['name']
		id = flask.request.form['id']
		score = flask.request.form['score']
		error = None
     
		with sqlite3.connect('players.db') as players:
			cursor = players.cursor()
			cursor.execute('UPDATE players SET name = ?, id = ?, score =? WHERE i =?',(name, id, score, i))
			players.commit()
		return index()
	else:
		return flask.render_template('/update.html')


@APP.route('/search')

def search():
	return flask.render_template('/search.html')

@APP.route('/result', methods=('POST',))
def result():
	id=flask.request.form.get("id")
	with sqlite3.connect('players.db') as players:
		conn = get_db_connection()
		#cursor = players.cursor()
		#data = cursor.execute("SELECT * FROM players WHERE name LIKE ?", ("%"+search+"%",))
		data = conn.execute('SELECT * FROM players WHERE id = ?',(id,))
		if data is None:
			abort(404, f"Player not found.")
		return flask.render_template('/result.html', headings=headings, players = data)

def getusers(search):
	conn = get_db_connection()
	cursor = conn.cursor()
	check=cursor.execute(
			"SELECT * FROM players WHERE name LIKE ? OR id LIKE ?", ("%"+search+"%", "%"+search+"%",)
		)
	results = cursor.fetchall()
	conn.close()
	return results


@APP.route('/about')

def about():
	return flask.render_template('/about.html')

@APP.route('/refresh')

def refresh():
	init_db.init()
	return index()


if (__name__ == '__main__'):
	APP.run()
