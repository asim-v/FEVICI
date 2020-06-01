## export FLASK_APP=application.py
## export FLASK_ENV=development
from flask import Flask, render_template, request, session, send_file, send_from_directory, safe_join, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session
import datetime
from flask_firebase import FirebaseAuth
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

#import proyectos
#variable = proyectos.coordenada(1)
#print(variable.a)


#Variable called session which can be used to store values specific to each user

import csv
import os

#Sessions, init flask
app = Flask(__name__)
Session(app)

app.config['FIREBASE_API_KEY'] = ''
app.config['FIREBASE_PROJECT_ID'] = ''
app.config['FIREBASE_AUTH_SIGN_IN_OPTIONS'] = 'email'

db = SQLAlchemy(app)
auth = FirebaseAuth(app)
login_manager = LoginManager()

login_manager.init_app(app)

app.register_blueprint(auth.blueprint, url_prefix='/auth')


class Account(UserMixin, db.Model):
    __tablename__ = 'accounts'
    account_id = db.Column(db.Integer, primary_key=True)
    firebase_user_id = db.Column(db.Text, unique=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    name = db.Column(db.Text)
    photo_url = db.Column(db.Text)


@auth.production_loader
def production_sign_in(token):
    account = Account.query.filter_by(firebase_user_id=token['sub']).one_or_none()
    if account is None:
        account = Account(firebase_user_id=token['sub'])
        db.session.add(account)
    account.email = token['email']
    account.email_verified = token['email_verified']
    account.name = token.get('name')
    account.photo_url = token.get('picture')
    db.session.flush()
    login_user(account)

@auth.unloader
def sign_out():
    logout_user()


@login_manager.user_loader
def load_user(account_id):
    return Account.query.get(account_id)


@login_manager.unauthorized_handler
def authentication_required():
    return auth.url_for('widget', mode='select', next=request.url)


@app.route('/')#Which page you want to request
def index():#Any name
	mensaje = "Saludos"
	return render_template("landing.html",mensaje = mensaje)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
