'''
Plataforma para FEVICI

Ete es el constructor de la aplicación, los endpoints correspondientes están en la carpeta apps y todos son inicialidados con sus librerías  cono init.py

TODO: 
    - Implementar Registro para profesores con un menú o tabla dinámica para visualziar solamente los proyectos de su interés y una pequeña descripción del proyecto, 
        Idealmente tiene la opción de verlo sin tener que descargarlo, embedido en otra página HTML
    - Implementar bloqueo de formularios
    - Interfaz para chats y chats recientes
    - Colocar correctamente la dashboard o la página de inicio, parecido al templete con la experiencia similar a esta:
        - https://demo.themewagon.com/preview/free-bootstrap-4-html5-admin-dashboard-template-adminmart
    - Colocar ventana de colaboradores,reglas, convocatoria, premios y recursos interactivos
    - Terminar Landing Page

EN PROGRESO:
    - Implementando funcionalidad para compartir proyecto (Link de vista pública y colaboradores)
    - Implementando descarga de archivos subidos.

Changelog:
    - (28/6) Formulario "Sobre Mi implementado"
    - (27/6) Formulario "Proyecto" implementado con subida de archivos
    - (20/6) Implementado sistema de mensajeado en tiempo real, falta implementar interfaz


''' 

#Basically initializes all the libraries that are common among the applications
from init import *


#Apps
from apps.chat import chatBP
from apps.login import loginBP
from apps.register import registerBP
from apps.calendar import calendarBP
from apps.expo import expoBP
from apps.about import aboutBP
from apps.project import projectBP
from apps.index import indexBP
from apps.teams import teamsBP


#INTI FLASK with socketio for rt msg
app = Flask(__name__)
app.secret_key = b'\xbd\x93K)\xd3\xeeE_\xfb0\xa6\xab\xa5\xa9\x1a\t'

#Registra Blueprints
app.register_blueprint(chatBP)
app.register_blueprint(loginBP)
app.register_blueprint(registerBP)
app.register_blueprint(calendarBP)
app.register_blueprint(expoBP)
app.register_blueprint(aboutBP)
app.register_blueprint(projectBP)
app.register_blueprint(indexBP)
app.register_blueprint(teamsBP)




#MAIL
#CONFIGURAR MAILSERVER
app.config['MAIL_SERVER'] = 'smtpout.secureserver.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'contacto@fevici.org'
app.config['MAIL_PASSWORD'] = '$#!(!_V)SADSa33'
# app.config['MAIL_DEFAULT_SENDER']
app.config['MAIL_MAX_EMAILS'] = 2
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['TESTING'] = False
# app.config['MAIL_ASCII_ATTACHMENTS']
mail = Mail(app)


#Init Socketio
socketio = SocketIO(app, cors_allowed_origins="*")



@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


if (__name__ == "__main__"):
    #app.run(debug=True)
	socketio.run(app,host='0.0.0.0',debug=True)