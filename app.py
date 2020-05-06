## export FLASK_APP=application.py
## export FLASK_ENV=development
from flask import Flask, render_template, request, session, send_file, send_from_directory, safe_join, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session
import datetime
#Variable called session which can be used to store values specific to each user

import csv
import os

#Sessions, init flask
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["FLASK_ENV"] = "development"
app.config["FLASK_DEBUG"] = "1"
Session(app)

#db
engine = create_engine("postgres://nnqbaxqctagpvj:bf5ef956dfd46fafe21aae175693d4454a3e530bde9e82083de4fc81dcf8a06c@ec2-54-165-36-134.compute-1.amazonaws.com:5432/db7900r7fqp39s")#connection string
db = connection = engine.connect()


@app.route('/')#Which page you want to request
def index():#Any name
    return render_template("landing.html")


@app.route("/dashboard")
def dashboard():        
    return render_template("dashboard.html")