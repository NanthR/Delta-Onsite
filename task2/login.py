from flask import Flask, request, redirect, url_for, session, render_template, flash, session, make_response
import sqlite3
from os import urandom
from itsdangerous import TimedJSONWebSignatureSerializer as SZ
from forms import RequestReset, ChangePassword, Login
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt

app = Flask(__name__)

conn = sqlite3.connect("login.db", check_same_thread=False)

global COOKIE_TIMEOUT
COOKIE_TIMEOUT = 60

app.config.from_object('config')
app.secret_key = urandom(24)

mail = Mail(app)

@app.route("/", methods=["POST", "GET"])
def home():
	try:
		if session['Authenticated']:
			return redirect(url_for("main"))
	except:
		pass
	form = Login(request.form)
	if request.method == "POST":
		if "Forgot" in request.form:
			return redirect(url_for('reset'))
		cur = conn.cursor()
		cur.execute("SELECT password FROM Users WHERE user = ?", (form.username.data,))
		password = cur.fetchone()
		if password is None:
			return "User doesn't exist"
		else:
			bcrypt = Bcrypt()
			password = password[0]
			if bcrypt.check_password_hash(password, form.password.data):
				if form.remember.data:
					s = SZ(app.secret_key, COOKIE_TIMEOUT)
					token = s.dumps({'name':form.username.data, 'ip':request.remote_addr}).decode('utf-8')
					resp = make_response(redirect("/main"))
					resp.set_cookie('username', form.username.data, max_age=COOKIE_TIMEOUT)
					resp.set_cookie('token', token, max_age=COOKIE_TIMEOUT)
					return resp
				session['Authenticated'] = True
				return redirect(url_for("main"))
			else:
				return "Failure"
	else:
		if 'username' in request.cookies:
			cur = conn.cursor()
			s = SZ(app.secret_key)
			try:
				data = s.loads(request.cookies['token'])
			except:
				return render_template("login.html", form=form)
			if request.remote_addr == data['ip']:
				session['Authenticated'] = True
				return redirect(url_for("main"))
			else:
				flash('Login from different IP. Kindly login again')
		return render_template('login.html', form=form)

@app.route("/main")
def main():
	try: 
		if session['Authenticated'] == True:
			return "Authenticated"
	except:
		return redirect(url_for("home"))


@app.route("/password-reset", methods=["POST", "GET"])
def reset():
	form = RequestReset(request.form)
	if request.method == "POST":
		if form.validate():
			name = check_email(request.form['email'])
			if name == None:
				flash("No such user exists")
				return render_template("forgotten.html", form=form)
			else:
				token = serializer(name)
				msg = Message('Password Reset Request', sender = 'noreply@demo.com', recipients=[request.form['email']])
				msg.body = f'To reset your password, visit the following link:\n{url_for("reset_token", token=token, _external=True)}'
				print(msg)
				mail.send(msg)
				flash(f"Mail sent to {request.form['email']} with instructions")
				return redirect(url_for("home"))
		else:
			flash("Invalid Entry")
			return render_template("forgotten.html", form=form)
	else:
		return render_template("forgotten.html", form=form)

@app.route("/reset/<token>", methods=["POST", "GET"])
def reset_token(token):
	form = ChangePassword(request.form)
	s = SZ(app.secret_key)
	try:
		data = s.loads(token)
	except:
		flash("Error with reset link. Try again")
		return redirect(url_for("reset"))
	print(data)
	if request.method == "POST" and form.validate():
		cur = conn.cursor()
		bcrypt = Bcrypt()
		cur.execute("UPDATE Users SET password = ? WHERE user = ?", (bcrypt.generate_password_hash(request.form['password']).decode('utf-8'), data['name'][0]))
		cur.commit()
		return redirect(url_for("home"))
	else:
		return render_template("change_password.html", form=form)

def serializer(name):
	s = SZ(app.secret_key, expires_in=600)
	token = s.dumps({'name':name}).decode('utf-8')
	return token

def check_email(email):
	cur = conn.cursor()
	cur.execute("SELECT * FROM Users")
	print(cur.fetchall())
	cur.execute("SELECT user FROM Users WHERE email=?", (email, ))
	name = cur.fetchone()
	return name

def error():
	if request.form["UserName"] == "" or request.form["Password"] == "":
		return "Empty password or username"
	return None

if __name__ == "__main__":
	app.run(debug=True)
