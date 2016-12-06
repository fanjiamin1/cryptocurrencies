from db import db
x = db.cursor()

def transaction(t_from, t_to, t_amount, t_session):
	try:
		x.execute("INSERT INTO transaction (t_from, t_to, t_amount, t_session) VALUES (%s, %s, %s, %s)", 
		(t_from, t_to, t_amount, t_session))
		db.commit()
	except db.Error as e:
		print(e)
		db.rollback()
	
	return x.lastrowid

def look_up_transaction(t_id):
	try:
		x.execute("SELECT * FROM transaction WHERE t_id = %s", (t_id,))
		return x.fetchall()
	except:
		db.rollback()

def add_account():
	try:
		x.execute("INSERT INTO account (a_id) VALUES (null)")
		db.commit()
	except:
		db.rollback()

	return x.lastrowid

def remove_account(account_id):
	try:
		x.execute("DELETE FROM account WHERE a_id = %s", (account_id,))
		db.commit()
	except:
		db.rollback()