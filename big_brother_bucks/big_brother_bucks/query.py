from .db import db


x = db.cursor()


def transaction(t_from, t_to, t_amount, t_session):
	try:
		x.execute("INSERT INTO transaction (t_from, t_to, t_amount, t_session) VALUES (%s, %s, %s, %s)", 
		(t_from, t_to, t_amount, t_session))
		db.commit()
		return x.lastrowid
	except db.Error as e:
		db.rollback()
		return e

def look_up_transaction(t_id):
	try:
		x.execute("SELECT * FROM transaction WHERE t_id = %s", (t_id,))
		return x.fetchall()[0]
	except db.Error as e:
		db.rollback()
		return e

def add_account(a_pubkey):
	try:
		x.execute("INSERT INTO account (a_id, a_pubkey) VALUES (null, %s)", (a_pubkey,))
		db.commit()
		return x.lastrowid
	except db.Error as e:
		db.rollback()
		return e

def remove_account(account_id):
	try:
		x.execute("DELETE FROM account WHERE a_id = %s", (account_id,))
		db.commit()
		return x.lastrowid
	except db.Error as e:
		db.rollback()
		return e

def get_key(a_id):
	try:
		x.execute("SELECT a_pubkey FROM account WHERE a_id = %s", (a_id,))
		return x.fetchall()[0]
	except db.Error as e:
		return e
