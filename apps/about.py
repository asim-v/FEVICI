from init import *

aboutBP = Blueprint('aboutBP',__name__)


@aboutBP.route("/about")
def about():
    '''
        Renderiza el about form con el id del usuario en la sesion actual
    '''
    proj = users_coll.document(session['id']).get().to_dict()
    about_user= proj["about_user"]
    about_file = proj["about_file"]
    about_file_ID = proj["about_file"]["image_id"]
    session['about_file_ID'] = about_file_ID
    name = about_file['image_name'][:5]+'...'+about_file['image_name'][::-1][:3][::-1] 
    return render_template("about.html",user_name=session["user_name"],project = about_user,project_file = about_file,limit=limit,status = session['status'],active=2,name=name,profileid=session["about_file_ID"])



@aboutBP.route("/update_about", methods=["POST"])
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
                    if request.form[field] not in ['Ingresa Valor...','','Elegir categoría primero...']:  # Solo subir si no está vacio el formulario
                        data[field[0].upper()+field[1:]] = request.form[field]
                except Exception as e:return str(e)#;print(str(request.form[field]))


            if request.files['file'] and not allowed_image(request.files['file'].filename):
                save_json({"about_user":data})
                
                session["status"] = "Se guardaron los datos pero la imagen subida no es compatible, los formatos aceptados son PNG,JPG,JPEG"
                return redirect(url_for("aboutBP.about"))  

            else:                
                #Obtener spec para guardar
                user_doc = users_coll.document(session['id'])
                project_details = user_doc.get().to_dict().get("about_file")

                try:
                    #Save file devuelve el id del archivo que se guarda con la func
                    project_details["image_id"] = save_file(request.files['file'])              
                    project_details["image_name"] = request.files['file'].filename
                except:pass

                #return save_file(request.files['file']) #DEBUG
                save_json({"about_file":project_details})  #Guardar el nuevo data con el id agregado                
                save_json({"about_user":data})  #Guardar el data parseado de los forms

                #guarda rque salio bien en status
                session["status"] = "Success"
                return redirect(url_for("aboutBP.about"))  

        except Exception as e:return "FORM EXCEPTION: "+str(e)
    else: return 

