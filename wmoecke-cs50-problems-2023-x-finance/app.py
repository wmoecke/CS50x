import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, STOCKS_QUERY, USERID_QUERY, USERNAME_QUERY

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    data = []
    grandTotal = 0

    # Get stock info from history
    rows = db.execute(STOCKS_QUERY, session["user_id"])

    # For each row (stock) returned
    for row in rows:
        # Lookup symbol in API
        response = lookup(row["symbol"])

        # Create template object
        obj = {
            "symbol": response["symbol"],
            "name": response["name"],
            "shares": row["shares"],
            "price": usd(response["price"]),
            "total": usd(float(response["price"]) * int(row["shares"]))
        }

        # Add template object to array
        data.append(obj)

        # Increment grand total with stock price X shares
        grandTotal += (float(response["price"]) * int(row["shares"]))

    # Query database for user id
    rows = db.execute(USERID_QUERY, session["user_id"])

    # Get current balance
    cash = float(rows[0]["cash"])

    # Totalize grand total
    grandTotal += cash

    # Send populated template back to user
    return render_template("index.html", data=data, cash=usd(cash), grandTotal=usd(grandTotal))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        # Ensure number of shares was submitted
        elif not request.form.get("shares"):
            return apology("missing shares", 400)

        # Ensure number of shares is a positive integer (non-floating number)
        # This was required because check50 complained about one test. :\
        # Proper validation is already being performed by the UI.
        try:
            if int(request.form.get("shares")) <= 0:
                return apology("shares must be a positive integer", 400)
        except ValueError:
            return apology("shares must be an integer", 400)

        # Lookup symbol in API
        data = lookup(request.form.get("symbol"))

        # Ensure symbol exists
        if data is None:
            return apology("invalid symbol", 400)

        # Calculate share price X amount of shares desired
        totalShares = float(data["price"]) * int(request.form.get("shares"))

        # Query database for user id
        rows = db.execute(USERID_QUERY, session["user_id"])

        # Get current balance
        cash = float(rows[0]["cash"])

        # Ensure no overdraw from current balance
        if cash < totalShares:
            return apology("can't afford", 400)

        # Update database
        db.execute("INSERT INTO history ('userid', 'symbol', 'shares', 'price', 'order', 'transacted') VALUES (?, ?, ?, ?, 'BUY', DATETIME('now'))",
                   session["user_id"], data["symbol"], request.form.get("shares"), data["price"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - totalShares, session["user_id"])

        # Message will appear in next redirect
        flash("Bought!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Redirect user to buy page
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    data = []

    # Get info from history table
    rows = db.execute("SELECT * FROM history WHERE userid = ? ORDER BY DATETIME(transacted) DESC", session["user_id"])

    # For each row (stock) returned
    for row in rows:
        # Create template object
        obj = {
            "symbol": row["symbol"],
            "shares": row["shares"],
            "price": usd(row["price"]),
            "order": row["order"],
            "transacted": row["transacted"]
        }

        # Add template object to array
        data.append(obj)

    # Send populated template back to user
    return render_template("history.html", data=data)


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
        rows = db.execute(USERNAME_QUERY, request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Redirect user to login page
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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        # Lookup symbol in API
        data = lookup(request.form.get("symbol"))

        # Ensure symbol exists
        if data is None:
            return apology("invalid symbol", 400)

        # Redirect to quoted page with appropriate values passed on
        return render_template("quoted.html", symbol=data["symbol"], name=data["name"], price=usd(data["price"]))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Redirect user to quote page
        return render_template("quote.html")


@app.route("/change_pwd", methods=["GET", "POST"])
@login_required
def change_pwd():
    """Change a user's password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure current password was submitted
        if not request.form.get("old-password"):
            return apology("must provide current password", 403)

        # Ensure new password was submitted
        elif not request.form.get("new-password"):
            return apology("must provide new password", 403)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must enter new password again", 403)

        # Ensure password and confirmation are a match
        elif request.form.get("new-password") != request.form.get("confirmation"):
            return apology("passwords don't match", 403)

        # Query database for userid
        rows = db.execute(USERID_QUERY, session["user_id"])

        # Ensure current password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("old-password")):
            return apology("invalid password", 403)

        # Insert new user into database
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(
            request.form.get("new-password")), session["user_id"])

        # Message will appear in next redirect
        flash("Password changed!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Redirect user to 'change password' page
        return render_template("change_pwd.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Query database for username
        rows = db.execute(USERNAME_QUERY, request.form.get("username"))

        # Ensure username is unique
        if len(rows) > 0:
            return apology("username already exists", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must enter password again", 400)

        # Ensure password and confirmation are a match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # Insert new user into database
        db.execute("INSERT INTO users ('username', 'hash') VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        # Query database for username
        rows = db.execute(USERNAME_QUERY, request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Message will appear in next redirect
        flash("Registered!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Redirect user to registry page
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        # Ensure number of shares was submitted
        elif not request.form.get("shares"):
            return apology("missing shares", 400)

        # Get stock info from history
        rows = db.execute(STOCKS_QUERY, session["user_id"])

        # For each row returned
        for row in rows:
            if row["symbol"] == request.form.get("symbol"):
                # Ensure not overselling shares
                if int(row["shares"]) < int(request.form.get("shares")):
                    return apology("too many shares", 400)

        # Lookup symbol in API
        data = lookup(request.form.get("symbol"))

        # Calculate share price X amount of shares desired
        totalShares = float(data["price"]) * int(request.form.get("shares"))

        # Query database for user id
        rows = db.execute(USERID_QUERY, session["user_id"])

        # Get current balance
        cash = float(rows[0]["cash"])

        # Update database
        db.execute("INSERT INTO history ('userid', 'symbol', 'shares', 'price', 'order', 'transacted') VALUES (?, ?, ?, ?, 'SELL', DATETIME('now'))",
                   session["user_id"], data["symbol"], request.form.get("shares"), data["price"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + totalShares, session["user_id"])

        # Message will appear in next redirect
        flash("Sold!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        data = []

        # Get stock info from history
        rows = db.execute(STOCKS_QUERY, session["user_id"])

        # For each row (stock) returned
        for row in rows:
            # Create template object
            obj = {
                "symbol": row["symbol"],
            }

            # Add template object to array
            data.append(obj)

        # Redirect user to sell page
        return render_template("sell.html", data=data)


@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    """Add cash to user's account"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure amount was submitted
        if not request.form.get("amount"):
            return apology("missing amount", 400)

        # Increase the user's cash by the amount entered
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", request.form.get("amount"), session["user_id"])

        # Message will appear in next redirect
        flash(usd(float(request.form.get("amount"))) + " was added to account.")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Redirect user to 'add cash' page
        return render_template("cash.html")
