import os
import random
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from random import randint

from helpers import apology, login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///records.db")


@app.route("/")
def index():

    top = db.execute("SELECT * FROM records ORDER BY id DESC LIMIT 1")
    second = db.execute("SELECT * FROM records ORDER BY id DESC LIMIT 1, 1")
    third = db.execute("SELECT * FROM records ORDER BY id DESC LIMIT 2, 1")
    return render_template("index.html", top = top, second = second, third = third)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "POST":
        if not request.form.get("song"):
            return apology("missing song")
        elif not request.form.get("artist"):
            return apology("missing artist")
        elif not request.form.get("date"):
            return apology("missing date")

        song = request.form.get("song")
        artist = request.form.get("artist")
        memory = request.form.get("memory")
        date = request.form.get("date")


        db.execute("INSERT INTO records(user_id, song, artist, memory, date) VALUES(:user_id, :song, :artist, :memory, :date)", user_id = session["user_id"], song = song, artist = artist, memory = memory, date = date)
        flash("Recorded!")
        return redirect("/timeline")
    else:
        return render_template("create.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Get username
    username = request.args.get("username")

    # Check for username
    if not len(username) or db.execute("SELECT 1 FROM users WHERE username = :username", username=username.lower()):
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/timeline")
@login_required
def timeline():
    records = db.execute("SELECT * FROM records WHERE user_id = :user_id ORDER BY date DESC", user_id=session["user_id"])

    return render_template("timeline.html", records=records)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    session.clear()

    return redirect("/login")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Add user to database
        id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                        username=request.form.get("username"),
                        hash=generate_password_hash(request.form.get("password")))
        if not id:
            return apology("username taken")

        # Log user in
        session["user_id"] = id

        # Let user know they're registered
        flash("Registered!")
        return redirect("/")

    # GET
    else:
        return render_template("register.html")



def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
