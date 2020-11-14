'''
Plataforma para FEVICI uwu

Este archivo es el constructor de la aplicación, los endpoints correspondientes están en la carpeta apps y todos son inicialidados con sus librerías  cono init.py

TODO: 
    - Ambos pueden ser completamente de lado de cliente, e incluso independientes del backend de python
        - Los recursos interactivos ya están listos pero falta implenentar una ventana en la landing page donde puedas
          ver la lista de recursos y ver una página dedicada solo a ellos.
        - Una página de blogcitos con la API de google drive o algo muy mainstream

    - Implementar Registro para profesores con un menú o tabla dinámica para visualziar solamente los proyectos de su interés y una pequeña descripción del proyecto, 
        Idealmente tiene la opción de verlo sin tener que descargarlo, embedido en otra página HTML
    - Implementar bloqueo de formularios
    - Interfaz para chats y chats recientes
    - Terminar Landing Page
        - Poner premios o cosas sencillitas, también un snapshot de los últimos posts
    - Funcionalidad para compartir proyecto (Link de vista pública [osea un link que los 
      participantes puedan compartir que muestre su proyecto])
    - Calendario con próximos eventos
    - Notificaciones 
        - Enviar al correo del registrado:
            Verificación de correo
            Notifiacciones de mensaje
            Fechas
            Eventos agregados como revisión
        - Tambier en la UI que se vea el puntito rojo si hay noticias
    
EN PROGRESO:
    
    - Implementando ventana de expo, con todos los proyectos y sus respectivas queries y AJAX

Major Changelog:

    - (15/10) 
        - Colocado correctamente la dashboard o la página de inicio, parecido al templete con la experiencia similar a esta: hopin.com
    - (10/10)
        - Bugfixes, Sidenav colapsable en moviles, particulas reparadas
    - (15/9)        
        - Agregado soporte de subida de archivos e imagenes
    - (28/6) Formulario "Sobre Mi actualizado implementado"
    - (27/6) Formulario "Proyecto" implementado con subida de archivos
    - (20/6) Implementado sistema de mensajeado en tiempo real, falta implementar interfaz
    - (19/6) Implementado registro y login con firebase auth


''' 

#Inicializa todas las librerias que son comunes en toda la aplicación
from init import *


#Endpoints
from apps.chat import chatBP #/chat/id
from apps.login import loginBP #/login
from apps.register import registerBP #/register
from apps.calendar import calendarBP #/calendar
from apps.expo import expoBP #/expo
from apps.about import aboutBP #/about
from apps.project import projectBP #/project
from apps.index import indexBP #/index
from apps.teams import teamsBP # Recive y envía invitaciones


#INTI FLASK with socketio for rt msg
app = Flask(__name__,instance_relative_config=True)
app.config.from_object('config') #Normal Config
app.config.from_pyfile('config.py') #Secret keys Config

#Registra Blueprints
#Cada app se inicializa con liberias y variables globales con init.py
app.register_blueprint(chatBP)
app.register_blueprint(loginBP)
app.register_blueprint(registerBP)
app.register_blueprint(calendarBP)
app.register_blueprint(expoBP)
app.register_blueprint(aboutBP)
app.register_blueprint(projectBP)
app.register_blueprint(indexBP)
app.register_blueprint(teamsBP)





#Init Socketio
socketio = SocketIO(app, cors_allowed_origins="*")



@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css',path)

@app.route('/visualizations/<path:path>')
def send_viz(path):
    return send_from_directory('templates/visualizations', path)


if (__name__ == "__main__"):
    
	socketio.run(app,host='0.0.0.0',debug=True)