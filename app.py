from flask import Flask, render_template, \
		request, session, redirect, url_for, flash
import os

master_username = "hello"
master_password = "password"

SESSION_KEY = "lol"

app = Flask(__name__)
app.secret_key = os.urandom(8)

SUCCESS = 0
BAD_USERNAME = 1
BAD_PASSWORD = 2

def authenticate(user, pwrd):
	if user == master_username:
		if pwrd == master_password:
			return SUCCESS
		return BAD_PASSWORD
	return BAD_USERNAME

@app.route("/")
def root():
	if SESSION_KEY in session:
		return redirect(url_for("welcome"))
	return render_template("index.html")

@app.route("/welcome")
def welcome():
	if SESSION_KEY in session:
		return render_template("welcome.html",
					username=session[SESSION_KEY])
	return redirect(url_for("root"))


@app.route("/auth", methods=["POST"])
def auth():
	if SESSION_KEY in session:
		return redirect(url_for("welcome"))
	
	status_code = authenticate(request.form["username"],
					request.form["password"])
	
	if status_code == SUCCESS:
		session[SESSION_KEY] = request.form["username"];
		return redirect(url_for("welcome"))
	elif status_code == BAD_USERNAME:
		flash("Bad Username")
		return redirect(url_for("root"))
	elif status_code == BAD_PASSWORD:
		flash("Bad Password")
		return redirect(url_for("root"))

@app.route("/logout", methods=["POST"])
def logout():
	if SESSION_KEY in session.keys():
		print "removed cookie"
		session.pop(SESSION_KEY)
	
	#url_for takes the name of a function
	return redirect(url_for("root"))

if __name__ == "__main__":
	app.debug = True
	app.run()
