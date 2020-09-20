
# imports for flask
from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify,send_from_directory,Blueprint
from flask_mail import Mail, Message
#For File Management
from werkzeug.utils import secure_filename

# imports for firebase
from firebase_admin import credentials, firestore, auth
import firebase_admin
import firebase
from google.cloud import storage
from google.oauth2 import service_account

import sys#DEBUG
import os#DEBUG

# custom lib
import firebase_user_auth

# realtime communication
from flask_socketio import SocketIO, emit, send

import requests
import datetime
import random

expoBP = Blueprint('expoBP',__name__)


@expoBP.route("/expo")
def expo():
    return render_template("expo.html",user_name=session["user_name"],status = session['status'],active=6,profileid=session["about_file_ID"])
