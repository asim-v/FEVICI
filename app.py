## export FLASK_APP=application.py
## export FLASK_ENV=development
from flask import Flask, render_template, request, session, send_file, send_from_directory, safe_join, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session
import datetime


import proyectos
variable = proyectos.coordenada(1)
print(variable.a)


#Variable called session which can be used to store values specific to each user

import csv
import os

#Sessions, init flask
app = Flask(__name__)
Session(app)


@app.route('/')#Which page you want to request
def index():#Any name
	mensaje = "Saludos"
	return render_template("landing.html",mensaje = mensaje)


@app.route("/dashboard")
def dashboard():        
    return render_template("dashboard.html")