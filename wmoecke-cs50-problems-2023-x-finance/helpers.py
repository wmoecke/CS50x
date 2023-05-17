import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

# Query used throughout the code to get stock info from history table
STOCKS_QUERY = """
    SELECT
        buy.symbol,
        (COALESCE(buy.shares, 0) - COALESCE(sell.shares, 0)) as shares,
        (COALESCE(buy.total, 0) - COALESCE(sell.total, 0)) as total
    FROM
        (SELECT userid, symbol, SUM(shares) as shares, SUM(shares * price) as total FROM history WHERE "order" = "BUY"  GROUP BY symbol) as buy
    LEFT JOIN
        (SELECT userid, symbol, SUM(shares) as shares, SUM(shares * price) as total FROM history WHERE "order" = "SELL"  GROUP BY symbol) as sell
        ON buy.symbol = sell.symbol
        AND buy.userid = sell.userid
    WHERE buy.userid = ?
    AND (COALESCE(buy.shares, 0) - COALESCE(sell.shares, 0)) > 0
"""
# Queries used throughout the code to get all info from users table
USERID_QUERY = "SELECT * FROM users WHERE id = ?"
USERNAME_QUERY = "SELECT * FROM users WHERE username = ?"


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"