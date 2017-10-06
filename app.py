from flask import Flask, render_template, \
		request, session, redirect, url_for
import os

master_username = "hello"
master_password = "password"

SESSION_KEY = "lol"

app = Flask(__name__)
app.secret_key = os.urandom(8)

@app.route("/", methods=["GET", "POST"])
def root():
	username = ""
	password = ""
	
	if SESSION_KEY in session:
		return render_template("index.html", 
				username=session[SESSION_KEY])
	
	if request.method == "GET":
		if request.args:
			username = request.args["username"]
			password = request.args["password"]
		else:
			return render_template("index.html")

	elif request.method == "POST":
		if request.form:
			username = request.form["username"]
			password = request.form["password"]
		else:
			return render_template("index.html")
	
	if username == "" or username != master_username:
		return render_template("index.html", bad_username=True)
	
	if password == "" or password != master_password:
		return render_template("index.html", bad_password=True)
	
	session[SESSION_KEY] = username
	
	return render_template("index.html", 
				username=username)

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
