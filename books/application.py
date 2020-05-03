import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session,redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
import requests
import json
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import login_required
import time


app = Flask(__name__)

#KEY = 6Ujajpd77OyRpdnQWf6rBA
API_KEY="6Ujajpd77OyRpdnQWf6rBA"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
SQLALCHEMY_ENGINE_OPTIONS = {
    "max_overflow": 15,
    "pool_pre_ping": True,
    "pool_recycle": 60 * 60,
    "pool_size": 30,
}

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():
	usr = db.execute("SELECT * FROM users WHERE id = :id", {"id": session.get("userid")}).fetchone()
	return render_template("index.html",username=usr['username'])

@app.route("/login", methods=["GET","POST"])
def login():
	session.clear()
	if request.method == "GET":
		return render_template("login.html")

	if not request.form.get("username") or not request.form.get("password"):
		return render_template("error.html",message="Username and/or password missing.")

	usr = db.execute("SELECT * FROM users WHERE username = :username AND password=:password", {"username": request.form.get("username"),"password":request.form.get("password")}).fetchone()
	
	try:
		if len(usr) > 0:
			session["userid"] = usr['id'] #SUCCESS
			return redirect("/")
	except:
		return render_template("error.html",message="Username/password incorrect.")



@app.route("/register", methods=["GET","POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")

	if not request.form.get("username"): 
		return render_template("error.html",message="Username missing.")
	elif  not request.form.get("password") or not request.form.get("confirm"):
		return render_template("error.html",message="Password and/or confirmation missing.")

	#check if password and confirmation match
	if request.form.get("password") != request.form.get("confirm"):
		return render_template("error.html",message="Password and confirmation don't match.")

	#check if username already exists
	if 	db.execute("SELECT id FROM users WHERE username = :username", {"username": request.form.get("username")}).rowcount > 0:
		return render_template("error.html",message="Username already exists.")

	#successful registration
	username=request.form.get("username")
	db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",{"username": request.form.get("username"), "password": request.form.get("password")})
	db.commit()
	usr = db.execute("SELECT * FROM users WHERE username = :username", {"username": request.form.get("username")}).fetchone()
	session["userid"]= usr['id']
	return redirect("/")


@app.route("/search")
@login_required
def search():

	searchfor = request.args.get("q")
	if searchfor is None:
		searchfor=""

	if not request.args.get("q"):
		res = db.execute( "SELECT * FROM books").fetchall() 
	else:
		res = db.execute( "SELECT * FROM books WHERE (isbn ILIKE :searchfor OR title ILIKE :searchfor OR author ILIKE :searchfor)" , {"searchfor":"%"+searchfor+"%"} ).fetchall()
		if len(res)==0 :
			return render_template("error.html",message="No results found.")

	return render_template("results.html",res=res,searchfor=searchfor,lenres=len(res))

	#return redirect("/")

@app.route("/book",methods=["GET","POST"])
@login_required
def book():
	if request.method =="GET":
		res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": API_KEY, "isbns":request.args.get("isbn") }).json()
		data=res["books"][0]
		book = db.execute("SELECT * FROM books WHERE isbn= :isbn",{"isbn":request.args.get("isbn")}).fetchone()
		if book is None:
			return render_template("error.html",message="ISBN number invalid.")
		#get reviews	
		reviews = db.execute("SELECT * FROM users INNER JOIN reviews ON reviews.reviewer = users.id WHERE bookid= :isbn",{"isbn":request.args.get("isbn")}).fetchall()
		if len(reviews) ==0:
			reviews = None

		#check if user already reviewed
		reviewed= db.execute("SELECT * FROM reviews WHERE reviewer = :userid AND bookid=:bookid", {"userid": session.get("userid"),"bookid":request.args.get("isbn")}).fetchone()
		if reviewed is None:
			reviewed=False
		else:
			reviewed=True


		return render_template("book.html",book=book,data=data,reviews=reviews,reviewed=reviewed)
	else:
		db.execute("INSERT INTO reviews (reviewer,review,rating,bookid) VALUES (:userid,:review,:rating,:bookid)",{"userid": session.get("userid"), "review": request.form.get("review"),"rating":request.form.get("rating") ,"bookid": request.form.get("bookid")})
		db.commit()
		url = "/book?isbn=" + request.form.get("bookid")
		return redirect(url)

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")


if __name__ == '__main__':
	app.debug=True
	app.run()


