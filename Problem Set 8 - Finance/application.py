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
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Formating into money type
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.2f}".format(value)

@app.route("/")
@login_required
def index():
    """Show the index page"""
    # Searching for the current cash from user
    current_cash = db.execute(f"SELECT cash FROM users WHERE id = {session['user_id']}")

    stocks = db.execute(f"SELECT * FROM stocks WHERE userid = {session['user_id']}")

    # Getting the stocks + current cash sum
    total_sum = db.execute(f"SELECT sum(total) as total FROM stocks WHERE userid = {session['user_id']}")

    if total_sum[0]['total'] == None:
        total = current_cash[0]['cash']
    else:
        total = total_sum[0]['total'] + current_cash[0]['cash']

    return render_template("index.html", current_cash = current_cash[0]['cash'], stocks = stocks, total = total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == 'GET':
        return render_template("buy.html")

    else:
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        elif not request.form.get("shares"):
            return apology("missing shares", 400)

        symbol = lookup(request.form.get("symbol"))

        if not symbol:
            return apology("invalid stock symbol", 400)

        else:
            # Getting the Buy values
            stockname = symbol['name']
            stocksymbol = symbol['symbol']
            shares = float(request.form.get("shares"))
            price = symbol['price']
            total = shares * price

            # Checking if the user can not afford a stock
            cash = db.execute(f"SELECT cash FROM users WHERE id = {session['user_id']}")

            if cash[0]['cash'] < total:
               return apology("can't afford", 400)

            else:
                # Checking if a company name alredy exists
                search_db = db.execute(f"SELECT count(stockname) as sn FROM stocks WHERE userid = {session['user_id']} and stockname = '{stockname}'")

                if search_db[0]['sn'] == 0:
                    db.execute(f"INSERT INTO stocks (userid, stockname, stocksymbol, price, date) VALUES ({session['user_id']}, '{stockname}', '{stocksymbol}', '{price}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')")

                # Updating the values
                db.execute(f"UPDATE users SET cash = cash - {total} WHERE id = {session['user_id']}")
                db.execute(f"UPDATE stocks SET shares = shares + {shares} WHERE userid = {session['user_id']} AND stockname = '{stockname}'")
                db.execute(f"UPDATE stocks SET total = total + {total} WHERE userid = {session['user_id']} AND stockname = '{stockname}'")
                db.execute(f"UPDATE stocks SET date = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE userid = {session['user_id']} AND stockname = '{stockname}'")

                # Redirect to the index page
                return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks = db.execute(f"SELECT * FROM stocks WHERE userid = {session['user_id']}")
    return render_template("history.html", stocks = stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
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
    if request.method == 'GET':
        return render_template("quote.html")

    else:
        if not request.form.get("quote"):
            return apology("must provide symbol", 403)

        symbol = request.form.get("quote")

        quote = lookup(symbol)

        if not quote:
            return apology("Stock not found", 400)

        else:
            return render_template('quoted.html', quote = quote)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    else:
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirm password was submitted
        elif not request.form.get("confirm_password"):
            return apology("must provide a password confirmation", 403)

        username = request.form.get("username")

        password = request.form.get("password")

        password_confirm = request.form.get("confirm_password")

        # Check if username already exists
        check_username = db.execute(f"SELECT count(*) FROM users WHERE username = '{username}'")

        if check_username[0]['count(*)'] > 0:
            return apology("username already exists", 403)

        # Check if password match with its confirmation
        elif password != password_confirm:
            return apology("password not match with confirmartion password", 403)

        else:
            hash_password = generate_password_hash(request.form.get("password"))

            db.execute(f"INSERT INTO users (username, hash) VALUES('{username}', '{hash_password}')")

            return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    search_symbols = db.execute(f"SELECT stocksymbol FROM stocks WHERE userid = {session['user_id']}")

    if request.method == 'GET':
        return render_template("sell.html", stocksymbols = search_symbols)

    else:
        sell_symbol = request.form.get("symbol")

        if not sell_symbol:
            return apology("missing stock symbol", 400)

        sell_shares = request.form.get("shares")
        search_shares = db.execute(f"SELECT shares FROM stocks WHERE userid = {session['user_id']}")

        if int(sell_shares) > search_shares[0]['shares']:
            return apology("too many shares", 400)

        else:
            sell_total = db.execute(f"SELECT (shares * price) as total FROM stocks WHERE userid = {session['user_id']} AND stocksymbol = '{sell_symbol}'")
            db.execute(f"UPDATE stocks SET shares = shares - {sell_shares} WHERE userid = {session['user_id']} AND stocksymbol = '{sell_symbol}'")
            db.execute(f"UPDATE users SET cash = cash + {sell_total[0]['total']} WHERE id = {session['user_id']}")
            db.execute(f"UPDATE stocks SET total = (shares * price) WHERE userid = {session['user_id']} AND stocksymbol = '{sell_symbol}'")
            db.execute(f"DELETE FROM stocks WHERE shares = 0 AND userid = {session['user_id']}")
            db.execute(f"UPDATE stocks SET date = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE userid = {session['user_id']} AND stocksymbol = '{sell_symbol}'")

            # Redirect to the index page
            return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)