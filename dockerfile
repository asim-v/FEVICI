# 1 
FROM python:3.6

# 2 
RUN pip install pycryptodome==3.6.6 werkzeug==0.16.0 flask_mail flask firebase_admin firebase gcloud flask_socketio firebase_user_auth requests requests_toolbelt
RUN pip install Flask gunicorn gspread oauth2client pandas flask_session flask_bcrypt flask_login firebase_admin flask-wtf peewee email_validator python_jwt sseclient

# 3
COPY / /app
WORKDIR /app

# 4
ENV PORT 8080

# 5
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app