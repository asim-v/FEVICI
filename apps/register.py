
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



# firebase user auth init
WEB_API_KEY = "AIzaSyCwvUgLW2pKUta-Me4oMi-JYumzAfavtcs"
user_auth = firebase_user_auth.initialize(WEB_API_KEY)


registerBP = Blueprint('registerBP',__name__)


@registerBP.route('/register', methods=["GET", "POST"])
def user_register():
    def genID():return int(random.random()*1000000)
    if (request.method == "POST"):
        user_name = request.form['userName']
        user_email = request.form['userEmail']
        user_password = request.form['userPassword']
        flash_msg = None
        try:
            user_recode = user_auth.create_user_with_email_password(user_email, user_password)
            # get idToken
            user_id_token = user_recode.get('idToken')
            # get a session cookie using id token and set it in sessions
            # this will automatically create secure cookies under the hood
            user_session_cookie = auth.create_session_cookie(user_id_token, expires_in=datetime.timedelta(days=14))           
            session['session_id'] = user_session_cookie
            # add user document to users collection
            session["id"] = user_recode.get('localId')
            users_coll.add({"name": user_name,
                            "email": user_email,
                            "team_id": genID(),
                            "about_user":{},
                            "about_file":{
                                "image_id":"default.png",
                                "image_name":"default.png"
                            },
                            "connected_chats": [],
                            "project_desc":{},
                            "project_file":{"project_id":0,"project_team":[session['id']],"project_name":''}
            }, user_recode.get('localId'))
            
            # if registration is valid then redirect to index page
            return redirect(url_for('indexBP.index_page'))
        except requests.HTTPError as e:
            if ("EMAIL_EXISTS" in str(e)):
                flash_msg = "Ya te registraste! Por favor inicia sesión."
            elif ("INVALID_EMAIL" in str(e)):
                flash_msg = "Por favor ingresa un correo electrónico válido"
            elif ("WEAK_PASSWORD" in str(e)):
                flash_msg = "Por favor utiliza una contraseña segura"
            else:
                flash_msg = "Algo salio mal!!"+str(e)        
            flash(flash_msg)
    # return to login page for GET
    return redirect(url_for('indexBP.user_login'))
