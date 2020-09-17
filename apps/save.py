def save_json(data,uid = None):
    '''
        INPUT = dict
        Guardar data json en id[default el de la sesion] de la bd, se hace la asignacion de este modo para evitar el sessionoutofcontext error
    '''
    try:
        u_id = session['id'] if (uid == None) else uid
        user_doc = users_coll.document(u_id)
        user_doc.update(data)
    except:
        return 'Save_json error'

def save_file(file,uid = None):
    '''
        Dado objeto file, guardar en base de datos fevici en proyectos
        Devuelve el id de donde ha sido guardado
    '''
    # gets the id of he old file to delete it
    user_doc = users_coll.document(session['id'])
    user_details = user_doc.get().to_dict()   
    try:
        project = user_details.get("project_file")['project_id']
        blob = bucket.blob(project) 
        blob.delete()
    except Exception as e:pass
    # gets the old file and deletes it
    

    new_filename = ''.join([str(int(random.random()*1000000))])                    
    while new_filename in all_projects: new_filename = ''.join([str(int(random.random()*1000000))])                    
        
    old_filename = file.filename

    extension = old_filename.rsplit('.', 1)[1].lower()
    blob = bucket.blob(new_filename+'.'+extension) 
    blob.upload_from_file(file)    


    return new_filename+'.'+extension

