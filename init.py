
# imports for flask
from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify,send_from_directory,Blueprint,jsonify
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

#regular code library made for parsing the forms to json
from apps.save import *



CONFIG = {
  "type": "service_account",
  "project_id": "fevici",
  "private_key_id": "e000820a21072e9d6c6d97cf922b1f1460e04cbb",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDMrH6C3GE917Sh\nND1e3nmA0idmYkTH2F9cBx3XKXY1JKLfwWw5P5U1qjtHJ2yTL/APFtOr4wrszJK8\n9eNwEwcbyAIVoewXGqK/0MSKCIoT9gLw+eVWJKPJV+5cm+7qnsRRnJ4KQ1TIywk0\nJNp4kF9ADIdeJy8kERiXizUpNuL5we2XBPr+oVxlJWoDaPwks2TMWQtLXNezxIZA\nFBy/Quy41NVMf34P424LQdDUbJSYsHzsTnHZ+6Zy9smy+PvM8rwn81OkDTRjHs2h\nSVO0B2ukVsDeEw9dtVnt3kN3ogZe5fe3TdFfKi13B1+pH0T0k9O2IvJKG5PnDipK\nBAm0gZEZAgMBAAECggEAA+oqs0sOyxWEnW6328gqj8W1PjaT9TSUwlhagEKJQcP1\nH41+CexG6NNcNeSxpXENyOQZYVjC3TuedOHJG1wpzyS4sXw63UhDo6KVF8TJC0+x\nx7Un50llHpVBeGD9JVyrCZqSxUR7aynC/83Speqw/7MdpbXfJ3PyQffGKQclOTyt\nEl3P047HXjpdhPIuKDw1g+gYbZZtItIkMa4IayY0nW0SBmk7CAktHEqTZdqzokHy\nMlieBmfZF3PoDQhme637ukzXUBHJOi5tiE3QTv+TvrBsQx06F7Iaq51mB12NR3ns\novm9rSucDUcJKTTKI4I6OJGXf7QxDD8NdS0kQu9leQKBgQDnx4BsStDMu2UnlhbW\nTjKoVoIu5FJsavjiMgGWCBHQR04ST/0MBAGG/3loYXiCfFichESkYr7/gD9ae5/V\n2WBPsWrwaQlRZULvEfkzX/SXsLUq3I8rwjRDBIyhxp5HHvO3+SoAI7+mgMqj6xOR\nUNokIOaaAYlp/N1BExw/tcfRvQKBgQDiD9+akwO8SRp6UmyTA95s/e9MyvAhTaPq\nWJG9g38spxk0B8rBBz6xv8Wcvufr7akrMkMdapnH3pm37w+5l5L0Azte257V01kE\nf7iQ5YHg3aR0gUMbRoFSMehsvhGa5DTN5+343tekSqrtUgTkSXvcJXWD02g+3GKZ\nUIQJSkH8jQKBgFobHvv6oe3VtF+NY9dwkxUKfJXKQZjQhW06T4+KF5LHBbzsx81S\nCV34F7TSn8zqlnBSo3TcxrABpZ+BjAPQ/DY/HPnVe7/fBAR5Ek48sZP/KI8/K5Gx\ncCvVqu6BjqrLh6gv/3oKa8lJLH5JN1Q5AHUnLT8V9dv0Z/eSfFrwSnxpAoGBAMba\ncbY2FjYdFCZ/tLRJ1fGIGmUxqrOQ6VxuVp0fO9Jalsf3Brpvlg2jhMASCk61u3ac\n+v64U9fGDvAGYY2/MGxnH2WcyQaMqCRV+VO0H2Bfd5doUVB/36ge8LYfJ7tZfL2X\ng/TEiWoiqGKkIFtz7HlFli7E21FYaX81nT/Sy2LNAoGAEWDKke6ROieFnyA0+JTg\nebu0iIITiPZ9CYq4Z9aR5ipaEnJK5E5WqrMLLsj7AxrxN9dup78GFEt1VE2mMEBv\ngCbVJIAYX2FnlP5TRhgGEuXIkRXFBAWUG8hsRG3hu5Gzzd18UmsT8idHFKKzQ3Kk\nvEunZN7Hq1ndewj2jVRFFhI=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-7as5m@fevici.iam.gserviceaccount.com",
  "client_id": "112005939490534307018",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-7as5m%40fevici.iam.gserviceaccount.com"
}




limit = "30 de Junio"
editable = True


# firebase user auth init
WEB_API_KEY = "AIzaSyCwvUgLW2pKUta-Me4oMi-JYumzAfavtcs"
user_auth = firebase_user_auth.initialize(WEB_API_KEY)
# keeping already watching list
chats_watch_list = {}



# initializes fb with bucket name
cred = credentials.Certificate(CONFIG)
default_app = firebase_admin.initialize_app(cred,{
    'storageBucket': 'fevici.appspot.com'
})
# configure buckets

credentials = service_account.Credentials.from_service_account_info(CONFIG)
client = storage.Client(project='fevici', credentials=credentials)

bucket = client.get_bucket('fevici.appspot.com')


#SIRVE PARA PROBAR COMO GUARDAR FILES
# blob = bucket.blob('my-test-file.txt')
# blob.upload_from_string('this is test content!')

#SIRVE PARA LISTAR LOS BLOBS QUE EXISTEN
# for blob in client.list_blobs('fevici.appspot.com', prefix='abc/myfolder'): #Con prefijo
# all_projects = [blob.name for blob in client.list_blobs('fevici.appspot.com')]
# print(all_projects)


#Db references
client = firestore.client()
# users collection reference 
users_coll = client.collection(u"users")
# notes collection reference
chats_coll = client.collection(u"notes")


