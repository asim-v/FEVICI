from init import *



projectBP = Blueprint('projectBP',__name__)

class team(object):
    def __init__(self,id):
        self.doc = user_doc = users_coll.document(id)
        self.name = user_doc.get().to_dict().get("name")
        self.email = user_doc.get().to_dict().get("email")
        self.color = random.choice(["#6772E5","#D869D0","#FF71A6","#FF967B","#FFC761"])
        self.initials = ''.join([x[0].upper() for x in self.name.split(' ')][:3])


@projectBP.route("/project")
def project():
    '''
        Renderiza el proyecto con el id del usuario en la sesion actual
    '''
    proj = users_coll.document(session['id']).get().to_dict()
    proj_desc= proj["project_desc"]
    proj_file = proj["project_file"]

    about_file_ID = proj["project_cover"]["image_id"]
    session['project_cover_ID'] = about_file_ID

    #generates team list object for visualizing teammates
    team_list = [team(x) for x in proj_file["project_team"]]

    return render_template("project.html",user_name=session["user_name"],team_list = team_list,project = proj_desc,limit=limit,status = session['status'],proj_file = proj_file,active=5,profileid=session["about_file_ID"],coverid=session["project_cover_ID"])


@projectBP.route("/update", methods=["POST"])
def update():    
    '''
        - Genera un dicionario con los formularios que se obtienen en el request con las llaves iguales al nombre del formulairo pero en mayuscula para guardarse en la bd:
        {'Nombre':nombre,...}
        - El formulario está hecho para tener dentro la información previa del usuario 
    '''
    def verifyForm(form):       
        data = {}
        for field in form: 
            try:
                if request.form[field] not in ['Ingresa Valor...','','Elegir categoría primero...']:  
                     # Solo subir si no está vacio el formulario
                    data[field[0].upper()+field[1:]] = request.form[field]
            except Exception as e:return str(e)#;print(str(request.form[field]))        


    if request.method == "POST":
        try: 

            
            form = request.form
            data = verifyForm(form)

            try:
                #Obtener spec para guardar
                user_doc = users_coll.document(session['id'])                                    
            except Exception as e:return "DB error"+str(e)


            # return jsonify(str(request.files))
            try:file = request.files['file'].filename                
            except:file = ''
            try:image = request.files['thumbnail'].filename
            except:image = ''


            if allowed_image(image):
                try:                
                    project_cover = user_doc.get().to_dict().get("project_cover")
                    project_cover["image_id"] = save_file(request.files['thumbnail'])
                    project_cover["image_name"] = image
                    save_json({"project_cover":project_cover})
                except Exception as e:return "Thumbnail error"+str(e)
                
                session["status"] = "Success"
                return redirect(url_for("projectBP.project"))  


            if allowed_file(file):
                try:                
                    # return save_file(request.files['file']) #DEBUG
                    #Save file devuelve el id del archivo que se guarda con la func                    return jsonify(str(save_file(request.files['file'])))
                    project_details = user_doc.get().to_dict().get("project_file")
                    project_details["project_id"] = save_file(request.files['file'],doc=True)                                      
                    project_details["project_name"] = file                    
                    save_json({"project_file":project_details})  #Guardar el nuevo data con el id agregado                
                except Exception as e:return "Project File"+str(e)                                       
                session["status"] = "Success"
                return redirect(url_for("projectBP.project"))  

            
            if not allowed_file(file) and not allowed_image(image):
                save_json({"project_desc":data})            
                session["status"] = "Se guardaron los datos pero ninguno de los archivos son compatibles"
                return redirect(url_for("projectBP.project"))                  
                            

            try:                                                
                save_json({"project_desc":data})  #Guardar el data parseado de los forms                    
            except Exception as e:return "Json error"+str(e)

            #guarda rque salio bien en status
            session["status"] = "Success"
            return redirect(url_for("projectBP.project"))  

        except Exception as e:return "FORM EXCEPTION: "+str(e)
    else: return 
