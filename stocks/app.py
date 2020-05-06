import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Make sure API key is set
os.environ["API_KEY"]="pk_4f45272c8077484db26ab48c68335e58";
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    db = SQL("sqlite:///finance.db")
    user = db.execute("SELECT * from users WHERE id= :userid",userid=session.get("user_id"))
    transactions = db.execute("SELECT symbol,COUNT(*) FROM transactions WHERE buyer_id=:userid AND action=:action GROUP BY symbol",action="BUY/OWNED",userid=session.get("user_id"))
    
    summary=[]
    for transaction in transactions:
        stock = lookup(transaction["symbol"])
        total = usd(float(stock["price"])*int(transaction["COUNT(*)"]))

        summary.append({"symbol":stock["symbol"],"name":stock["name"],"shares":transaction["COUNT(*)"],"price":usd(stock["price"]),"total":total })        
    return render_template("index.html",cash=usd(user[0]["cash"]),summary=summary)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    db = SQL("sqlite:///finance.db")
    """Buy shares of stock"""
    if request.method=="GET":
        return render_template("buy.html")
    else:

        shares = int(request.form.get("shares"))

        if shares<1:
            return apology("Enter a valid number of shares.",403)
        else:     
            if not lookup(request.form.get("symbol")):
                return apology("Invalid stock symbol",403)
        
        #Successful REQUEST TO buy!:
        stock=lookup(request.form.get("symbol"))
        user = db.execute("SELECT * from users WHERE id= :userid",userid=session.get("user_id"))
        if int(request.form.get("shares")) * stock['price'] > user[0]["cash"]:
            return apology("You don't have enough money.")
        else:
            # enough money, can buy
            for q in range(0,int(request.form.get("shares"))):
                db.execute("INSERT INTO transactions (buyer_id,action,symbol,price,quantity,purchase_time) VALUES (:buyer_id,:action,:symbol,:price,:quantity,:purchase_time)",buyer_id=user[0]["id"],action="BUY/OWNED",price=stock['price'],quantity=1,purchase_time=datetime.today(),symbol=request.form.get("symbol"))
            
            new_balance= user[0]["cash"] - (int(request.form.get("shares")) * stock['price'])
            db.execute("UPDATE users SET cash=:cash where id=:userid",cash=new_balance,userid=session.get("user_id"))
            return redirect("/")




@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    my_db = SQL("sqlite:///finance.db")
    user = my_db.execute("SELECT * from users WHERE id= :userid",userid=session.get("user_id"))
    transactions = my_db.execute("SELECT * from transactions WHERE buyer_id= :userid",userid=session.get("user_id"))
    
    summary=[]
    for transaction in transactions:
        stock = lookup(transaction["symbol"])
        total = usd(float(stock["price"])*int(transaction["quantity"]))
        if transaction["action"] == "BUY/SOLD" or transaction['action'] == "BUY/OWNED":
            action = "BUY"
        else:
            action = transaction['action']
        summary.append({"time":transaction["purchase_time"],"action":action,"symbol":stock["symbol"],"name":stock["name"],"shares":transaction["quantity"],"price":usd(stock["price"]),"total":total })
        
    return render_template("history.html",cash=usd(user[0]["cash"]),summary=summary)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    db = SQL("sqlite:///finance.db")
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method =="GET":
        return render_template("quote.html")
    else:
        if not request.form.get("symbol"):
            return apology("Stock symbol missing",403)

    stock = lookup(request.form.get("symbol"))
    if(stock):
        return render_template("quoted.html",symbol=stock['symbol'],name=stock['name'],price=usd(stock['price']))
    else:
        return apology("Invalid stock symbol",403)




@app.route("/register", methods=["GET", "POST"])
def register():
    db = SQL("sqlite:///finance.db")
    if request.method == "GET":
        return render_template("register.html")

    else: #User reached via POST (registration form)

        #check if both usrname and pass entered:
        if not request.form.get("username"):
            return apology("You must select a username", 403)
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Must enter password and password confirmation", 403)

        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("Your password and confirmation don't match")

        rows = db.execute("SELECT * FROM users WHERE username = :username",username=request.form.get("username"))
        if len(rows)>0:
            return apology("Username already exists",403)
        else:   
        #user can be registered
            username=request.form.get("username")
            pswd=generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users (username,hash) VALUES(:username,:password)",username=username,password=pswd)
            rows = db.execute("SELECT * FROM users WHERE username = :username",username=request.form.get("username"))            
            session["user_id"] = rows[0]["id"]
            return redirect("/")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    symbols=[]
    db = SQL("sqlite:///finance.db")
    transactions = db.execute("SELECT symbol,COUNT(*) FROM transactions WHERE buyer_id=:userid AND action=:action GROUP BY symbol",action="BUY/OWNED",userid=session.get("user_id"))
    
    for transaction in transactions:
        symbols.append(transaction["symbol"])

    if request.method == "GET":
        return render_template("sell.html",symbols=symbols)

    stock = request.form.get("stock")
    quantity = int(request.form.get("shares"))
    if quantity<1:
        return apology("Enter a valid number of shares to sell.",400)

    #check if user has enough to sell
    owned = db.execute("SELECT symbol FROM transactions WHERE buyer_id=:userid AND action=:action AND symbol=:symbol",action="BUY/OWNED",userid=session.get("user_id"),symbol=stock)

    if len(owned) < quantity:
        return apology("You don't own enough stocks.",400)

    stocks = db.execute("SELECT * FROM transactions WHERE buyer_id=:userid AND action=:action AND symbol=:symbol LIMIT :quantity",action="BUY/OWNED",userid=session.get("user_id"),symbol=stock,quantity=quantity)
    symbol = stocks[0]["symbol"]
    data = lookup(symbol)
    price = int(data['price'])

    for sell in stocks:
        db.execute(f"UPDATE transactions SET action='BUY/SOLD' WHERE buyer_id={session.get('user_id')} AND action='BUY/OWNED' AND symbol=:symbol AND transaction_id=:id",symbol=symbol,id=sell["transaction_id"])
        db.execute("INSERT INTO transactions (buyer_id,action,symbol,price,quantity,purchase_time) VALUES (:buyer_id,:action,:symbol,:price,:quantity,:purchase_time)",buyer_id=sell["buyer_id"],action="SELL",price=sell["price"],quantity=1,purchase_time=datetime.today(),symbol=symbol)

    user = db.execute("SELECT * from users WHERE id= :userid",userid=session.get("user_id"))
    new_balance= user[0]["cash"] + (quantity * price)
    db.execute("UPDATE users SET cash=:cash where id=:userid",cash=new_balance,userid=session.get("user_id"))
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)



if __name__ == '__main__':
    app.debug = True
    app.run()