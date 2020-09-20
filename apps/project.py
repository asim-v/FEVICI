
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

projectBP = Blueprint('projectBP',__name__)



@projectBP.route("/project")
def project():
    '''
        Renderiza el proyecto con el id del usuario en la sesion actual
    '''
    proj = users_coll.document(session['id']).get().to_dict()
    proj_desc= proj["project_desc"]
    proj_file = proj["project_file"]

    #generates team list object for visualizing teammates
    team_list = [team(x) for x in proj_file["project_team"]]

    return render_template("project.html",user_name=session["user_name"],team_list = team_list,project = proj_desc,limit=limit,status = session['status'],proj_file = proj_file,active=5,profileid=session["about_file_ID"])

def allowed_file(filename):
    '''
        Extensión en extensiones permitidas?
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_image(filename):
    '''
        Extensión en extensiones permitidas?
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGES

@projectBP.route("/update", methods=["POST"])
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
                return redirect(url_for("projectBP.project"))  

            else:                
                try:
                    #Obtener spec para guardar
                    user_doc = users_coll.document(session['id'])
                    project_details = user_doc.get().to_dict().get("project_file")
                except Exception as e:return "DB error"+str(e)

                try:
                    # return save_file(request.files['file']) #DEBUG
                    #Save file devuelve el id del archivo que se guarda con la func                    
                    project_details["project_id"] = save_file(request.files['file'])              
                    project_details["project_name"] = request.files['file'].filename
                except Exception as e:pass
                    
                try:            
                    
                    save_json({"project_file":project_details})  #Guardar el nuevo data con el id agregado                
                    save_json({"project_desc":data})  #Guardar el data parseado de los forms
                except Exception as e:return "Json error"+str(e)

                #guarda rque salio bien en status
                session["status"] = "Success"
                return redirect(url_for("projectBP.project"))  

        except Exception as e:return "FORM EXCEPTION: "+str(e)
    else: return 
