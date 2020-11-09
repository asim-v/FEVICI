from init import *

import base64
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


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
    def ProcessImage(imgstring):
        '''
            IN> Image string in base64
            OUT> FileStorage object 
        '''
        class fwrap(object):    
            '''
                Wraps:
                    -filename:(str):the name of the file with the exteison
                    -stream(bytes):the bytes decoded base64 version
            '''
            def __init__(self,stream,filename):
                self.stream = stream
                self.filename = filename
        
        
        data = ''.join(str(x) for x in imgstring.split(',')[1:])
        file_data = base64.b64decode(data)
        ending = imgstring.split(';')[0].split('/')[1]
        filename = secure_filename('image'+'.'+ending)

        return fwrap(file_data,filename)
        # return FileStorage(stream=file_data, filename=filename,content_type='image/'+ending)  ##No Funciona!!!


    if request.method == "POST":
        try: 

            data = {}
            form = request.form
            res = []



            for field in form: 
                try:
                    if request.form[field] not in ['Ingresa Valor...','','Elegir categoría primero...']:  # Solo subir si no está vacio el formulario
                        if field == 'image':                             
                            image_file = ProcessImage(request.form[field])
                            # return str('image_file: '+str(image_file.stream))
                        else: data[field[0].upper()+field[1:]] = request.form[field]
                except Exception as e:return 'forms'+str(e)#;print(str(request.form[field]))

            # return str(type(image_file.stream))
            # return save_file(image_file) #DEBUG

            if image_file and not allowed_image(image_file.filename):

                save_json({"about_user":data})                
                session["status"] = "Se guardaron los datos pero la imagen subida no es compatible, los formatos aceptados son PNG,JPG,JPEG"
                return redirect(url_for("aboutBP.about"))  

            else:                
                #Obtener spec para guardar
                user_doc = users_coll.document(session['id'])
                project_details = user_doc.get().to_dict().get("about_file")

                try:
                    #Save file devuelve el id del archivo que se guarda con la func
                    project_details["image_id"] = save_file(image_file)              
                    project_details["image_name"] = image_file.filename
                except Exception as e:return jsonify(str(e))

                # return save_file(image_file) #DEBUG
                save_json({"about_file":project_details})  #Guardar el nuevo data con el id agregado                
                save_json({"about_user":data})  #Guardar el data parseado de los forms

                #guarda rque salio bien en status
                session["status"] = "Success"
                return redirect(url_for("aboutBP.about"))  

        except Exception as e:return "FORM EXCEPTION: "+str(e)
    else: return 

