'''
Plataforma para FEVICI

TODO: 
    - Implementar Registro para profesores con un menú o tabla dinámica para visualziar solamente los proyectos de su interés y una pequeña descripción del proyecto, 
        Idealmente tiene la opción de verlo sin tener que descargarlo, embedido en otra página HTML
    - Implementar bloqueo de formularios
    - Interfaz para chats y chats recientes
    - Colocar correctamente la dashboard o la página de inicio, parecido al templete
    - Colocar ventana de colaboradores,reglas, convocatoria, premios y recursos interactivos
    - Terminar Landing Page

EN PROGRESO:
    - Implementando funcionalidad para compartir proyecto (Link de vista pública y colaboradores)

Changelog:
    - (28/6) Formulario "Sobre Mi implementado"
    - (27/6) Formulario "Proyecto" implementado con subida de archivos
    - (20/6) Implementado sistema de mensajeado en tiempo real, falta implementar interfaz


'''




# imports for flask
from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify,send_from_directory
from flask_mail import Mail, Message
#For File Management
from werkzeug.utils import secure_filename

# imports for firebase
from firebase_admin import credentials, firestore, auth, storage
import firebase_admin
import firebase
import google.cloud.storage as gstorage

import sys#DEBUG
import os#DEBUG

# custom lib
import firebase_user_auth

# realtime communication
from flask_socketio import SocketIO, emit, send

import requests
import datetime
import random



ALLOWED_EXTENSIONS = {'pdf'}
limit = "30 de Junio"
editable = True
WEB_API_KEY = "AIzaSyCwvUgLW2pKUta-Me4oMi-JYumzAfavtcs"# read web api key from file


# firebase user auth init
user_auth = firebase_user_auth.initialize(WEB_API_KEY)
# keeping already watching list
chats_watch_list = {}

#INTI FLASK with socketio for rt msg
app = Flask(__name__)
app.secret_key = b'\xbd\x93K)\xd3\xeeE_\xfb0\xa6\xab\xa5\xa9\x1a\t'
socketio = SocketIO(app, cors_allowed_origins="*")

#MAIL
mail = Mail(app)
mail.init_app(app)

#CONFIGURAR MAILSERVER
# app.config['MAIL_SERVER'] = 
# app.config['MAIL_PORT']
# app.config['MAIL_USE_TLS']
# app.config['MAIL_USE_SSL']
# app.config['MAIL_DEBUG']
# app.config['MAIL_USERNAME']
# app.config['MAIL_PASSWORD']
# app.config['MAIL_DEFAULT_SENDER']
# app.config['MAIL_MAX_EMAILS']
# app.config['MAIL_SUPPRESS_SEND']
# app.config['MAIL_ASCII_ATTACHMENTS']



# initializes fb with bucket name
cred = credentials.Certificate('creds/firebase-config.json')
default_app = firebase_admin.initialize_app(cred,{
    'storageBucket': 'fevici.appspot.com'
})
# configure buckets
client = gstorage.Client.from_service_account_json('creds/firebase-config.json')
bucket = client.get_bucket('fevici.appspot.com')

#SIRVE PARA PROBAR COMO GUARDAR FILES
# blob = bucket.blob('my-test-file.txt')
# blob.upload_from_string('this is test content!')



#Db references
db = firestore.client()
# users collection reference 
users_coll = db.collection(u"users")
# notes collection reference
chats_coll = db.collection(u"notes")






def _on_snapshot_callback(doc_snapshot, changes, readtime):
    # need to send requried event to required people
    chatid = doc_snapshot[0].id
    socketio.emit(chatid, {'doc_updated': True})

@app.route('/')
def index_page():
    '''
        Pagina de inicio
    '''
    flash_msg = None
    if ("session_id" in session):
        try:
            # verify session_id
            decoded_clamis = auth.verify_session_cookie(session["session_id"])   
            #flash(decoded_clamis)
            session['email_addr'] = decoded_clamis['email']
            session['id'] = decoded_clamis['user_id']
            #session variable to indicate errors
            session["status"]  = None
            

            # Trying to implement users connected chats list            
            user_doc = users_coll.document(decoded_clamis['user_id'])
            user_details = user_doc.get().to_dict()
            connected_chats = user_details.get("connected_chats")
            session["user_name"] = user_details.get("name")
            #flash(decoded_clamis)

            connected_chats_list = []
            for i in connected_chats:
                connected_chats_list.append(i.get().to_dict())
            
            return render_template("index.html", user_email=session["email_addr"],user_name=session["user_name"], chats_list=connected_chats_list[::-1])
        except Exception as e:
            # if unable to verify session_id for any reason
            # maybe invalid or expired, redirect to login
            flash_msg = "Your session is expired!"
            return "INDEX EXCEPTION" + str(e)

    flash_msg = "Please Log In"
    flash(flash_msg)
    return redirect(url_for("user_login"))    

@app.route('/login', methods=["GET","POST"])
def user_login():
    if (request.method == "POST"):
        user_email = request.form['userEmail']
        user_password = request.form['userPassword']
        flash_msg = None
        try:
            user_recode = user_auth.sign_in_user_with_email_password(user_email, user_password)
            session["token"] = user_recode
            # get idToken
            user_id_token = user_recode.get('idToken')
            # get a session cookie using id token and set it in sessions
            # this will automatically create secure cookies under the hood
            user_session_cookie = auth.create_session_cookie(user_id_token, expires_in=datetime.timedelta(days=14))           
            session['session_id'] = user_session_cookie
            # if username passwd valid then redirect to index page
            return redirect(url_for('index_page'))

        except requests.HTTPError as e:
            if ("EMAIL_NOT_FOUND" in str(e)):
                flash_msg = "Please register before login"
            elif ("INVALID_EMAIL" in str(e)):
                flash_msg = "Please enter a valid email address"
            elif ("INVALID_PASSWORD" in str(e)):
                flash_msg = "Email or Password is wrong"
            else:
                flash_msg = "Something is wrong!!"
        flash(flash_msg)
    # return login page for GET request
    # 1 - Newton Fractal 
    # 2 - Fluid Cube
    # 3 - Bacteria Evolution
    # 4 - Hennophase
    # 5 - Game of life
    # 6 - Mica Cube
    # 7 - Mandelbrot set
    # 8 - Stars

    return render_template("login.html",auth = False,visualization = random.choice([1,2,3,4,5,6,7,8,9]))
    

@app.route('/register', methods=["GET", "POST"])
def user_register():
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
                            "about_user":[],
                            "connected_chats": [],
                            "project_desc":[],
                            "project_file":{"project_id":0,"project_team":[session['id']],"project_name":''}
            }, user_recode.get('localId'))
            
            # if registration is valid then redirect to index page
            return redirect(url_for('index_page'))
        except requests.HTTPError as e:
            if ("EMAIL_EXISTS" in str(e)):
                flash_msg = "You have already registerd! Please log in."
            elif ("INVALID_EMAIL" in str(e)):
                flash_msg = "Please enter a valid email address"
            elif ("WEAK_PASSWORD" in str(e)):
                flash_msg = "Please use a strong password"
            else:
                flash_msg = "Something is wrong!!"+str(e)        
            flash(flash_msg)
    # return to login page for GET
    return redirect(url_for('user_login'))

@app.route('/logout')
def user_logout():
    #session.pop('session_id', None)
    session.clear()
    return redirect(url_for('index_page'))

@app.route("/chat/<chatid>")
def user_chat(chatid):
    '''
        TODO: Hacer ventana de chats como la de cualquier app de mensajeo con los profesores registrados.
    '''
    try:
        chat_doc = chats_coll.document(chatid)
        chat_details = chat_doc.get().to_dict()

        # if user is not already joined then append him to users list
        if (session["email_addr"] not in chat_details.get("users")):
            chat_details.get("users").append(session["email_addr"])
            chat_doc.update(chat_details, option=None)

            # then append chat_doc to user's connected chats
            user_doc = users_coll.document(session['id'])
            user_details = user_doc.get().to_dict()
            user_details.get("connected_chats").append(chat_doc)
            user_doc.update(user_details, option=None)


        # start checking for changes. 
        if (chatid not in chats_watch_list):
            chat_watch = chat_doc.on_snapshot(_on_snapshot_callback)

        return (render_template("chat.html", users_list=chat_details.get("users"), logged_user=session["email_addr"], chatid=chatid, user_email = session["email_addr"]))
    except:
        return (redirect(url_for('user_login')))



@app.route("/recieve_invite/<invite_id>")
def recieve_invite(invite_id):
    '''
        TODO: Dos opciones de invitación:
            1) El usuario recibe un correo y es redirigido al about donde se muestra el código de invitación recibido
            2) El usuario utiliza el cógido de invitación que también se muestra en el popup de project para ingtesarlo manualmente 
    '''
    pass



@app.route("/send_invite")
def send_invite():
    '''
        La pagina genera un id de invitación que al ser usado por otro usuario, sobreescribe su proyecto con el id del proyecto con el del enviado
    '''
    invite_to = "emiliobot@hotmail.com"
    msg = Message("Hello",
                      sender="from@example.com",
                      recipients=[invite_to])
    msg.recipients = ["you@example.com"]
    msg.add_recipient("somebodyelse@example.com")
    msg = Message("Hello",
                  sender=("Me", "me@example.com"))

    assert msg.sender == "Me <me@example.com>"

    msg.body = "testing"
    msg.html = "<b>testing</b>"

    mail.send(msg)

class team(object):
    def __init__(self,id):
        self.doc = user_doc = users_coll.document(id)
        self.name = user_doc.get().to_dict().get("name")
        self.email = user_doc.get().to_dict().get("email")
        self.color = random.choice(["#6772E5","#D869D0","#FF71A6","#FF967B","#FFC761","#F9F871"])
        self.initials = ''.join([x[0].upper() for x in self.name.split(' ')])

@app.route("/about")
def about():
    '''
        Renderiza el about form con el id del usuario en la sesion actual
    '''
    proj = users_coll.document(session['id']).get().to_dict()
    about_user= proj["about_user"]

    return render_template("about.html",user_name=session["user_name"],project = about_user,limit=limit,status = session['status'])



@app.route("/update_about", methods=["POST"])
def update_about():    
    '''
        Actualiza el formulairo about
    '''
    if request.method == "POST":
        try: 

            data = {}
            form = request.form


            for field in form: 
                try:
                    if request.form[field] not in ['Select Country','']:  # Solo subir si no está vacio el formulario
                        data[field[0].upper()+field[1:]] = request.form[field]
                except Exception as e:return str(e)#;print(str(request.form[field]))

            #return str(data) #DEBUG
            #return save_file(request.files['file']) #DEBUG

            save_json({"about_user":data})  #Guardar el data parseado de los forms

            #guarda rque salio bien en status
            session["status"] = "Success"
            return redirect(url_for("about"))  

        except Exception as e:return "FORM EXCEPTION: "+str(e)
    else: return 



@app.route("/project")
def project():
    '''
        Renderiza el proyecto con el id del usuario en la sesion actual
    '''
    proj = users_coll.document(session['id']).get().to_dict()
    proj_desc= proj["project_desc"]
    proj_file = proj["project_file"]
    #generates team list object for visualizing teammates
    team_list = [team(x) for x in proj_file["project_team"]]

    return render_template("project.html",user_name=session["user_name"],team_list = team_list,project = proj_desc,limit=limit,status = session['status'],proj_file = proj_file)

def save_json(data,uid = None):
    '''
        INPUT = dict
        Guardar data json en id[default el de la sesion] de la bd, se hace la asignacion de este modo para evitar el sessionoutofcontext error
    '''
    u_id = session['id'] if (uid == None) else uid
    user_doc = users_coll.document(u_id)
    user_doc.update(data)

def save_file(file,uid = None):
    '''
        Dado objeto file, guardar en base de datos fevici en proyectos
    '''
    # gets the id of he old file to delete it
    user_doc = users_coll.document(session['id'])
    user_details = user_doc.get().to_dict()
    # return user_details   DEBUG
    try:
        project = user_details.get("project_file")['project_id']
        blob = bucket.blob(project) 
        blob.delete()
    except:pass
    # gets the old file and deletes it


    filename = ''.join([str(int(random.random()*1000000))])                    
    blob = bucket.blob(filename) 
    blob.upload_from_file(file)    

    return filename


def allowed_file(filename):
    '''
        Extensión en extensiones permitidas?
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/update", methods=["POST"])
def update():    
    '''
        - Genera un dicionario con los formularios que se obtienen en el request con las llaves iguales al nombre del formulairo pero en mayuscula para guardarse en la bd:
        {'Nombre':nombre,...}
        - El formulario está hecho para tener dentro la información previa del usuario 
    '''
    if request.method == "POST":
        try: 

            data = {}
            form = request.form


            for field in form: 
                try:
                    if request.form[field] not in ['Ingresa Valor...','','Elegir categoría primero...']:  # Solo subir si no está vacio el formulario
                        data[field[0].upper()+field[1:]] = request.form[field]
                except Exception as e:return str(e)#;print(str(request.form[field]))


            if request.files['file'] and not allowed_file(request.files['file'].filename):
                save_json({"project_desc":data})
                
                session["status"] = "Se guardaron los datos pero el archivo subido no es compatible, los formatos aceptados son PDF,DOCX"
                return redirect(url_for("project"))  

            else:                
                #Obtener spec para guardar
                user_doc = users_coll.document(session['id'])
                project_details = user_doc.get().to_dict().get("project_file")


                #Save file devuelve el id del archivo que se guarda con la func
                project_details["project_id"] = save_file(request.files['file'])              
                project_details["project_name"] = request.files['file'].filename

                
                #return save_file(request.files['file']) #DEBUG
                save_json({"project_file":project_details})  #Guardar el nuevo data con el id agregado                
                save_json({"project_desc":data})  #Guardar el data parseado de los forms

                #guarda rque salio bien en status
                session["status"] = "Success"
                return redirect(url_for("project"))  

        except Exception as e:return "FORM EXCEPTION: "+str(e)
    else: return 

@app.route("/new-chat")
def new_chat():
    return (render_template("new-note.html"))

@app.route("/new-chat/create")
def create_new_chat():
    try:
        cid = str(random.random())[2:] + str(random.randint(1241, 4124))
        chats_coll.add({"nid": cid,
                        "users": [],
						"chat": ""
        }, cid)
        return (redirect("/chat/{}".format(cid)))
    except:
	    return ("There is an error. Please try again.")
	

# get chatid and return chat_detail
@app.route("/chat/getinfo/<chatid>")
def get_chat_info(chatid):
    cht_info = chats_coll.document(chatid)
    session[chatid] = False	
    return (jsonify(cht_info.get().to_dict()))


@app.route("/chat/add/<chatid>/<message>")
def add_chat(chatid, message):

    chat_doc = chats_coll.document(chatid)
    chat_details = chat_doc.get().to_dict()
    chat_details["chat"] += "\n[{}] : {}".format(session.get("email_addr").split("@")[0], message)
    chat_doc.update(chat_details, option=None)

    # need to handle errors but for now
    return (jsonify({}))

@app.route("/chat/leave/<chatid>")
def leave_chat(chatid):
    try:
        chat_doc = chats_coll.document(chatid)
        chat_details = chat_doc.get().to_dict()
        chat_details.get("users").remove(session.get("email_addr"))
        chat_doc.update(chat_details, option=None)

        user_doc = users_coll.document(session["id"])
        user_details = user_doc.get().to_dict()
        user_details.get("connected_chats").remove(chat_doc)
        user_doc.update(user_details, option=None) 
        # just for now
        return redirect(url_for("index_page"))   
    except Exception as e:
        return (str(e))

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

if (__name__ == "__main__"):
    #app.run(debug=True)
	socketio.run(app, debug=True)