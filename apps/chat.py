from flask import Blueprint
from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify,send_from_directory

chat = Blueprint('chat',__name__)


@chat.route("/new-chat")
def new_chat():
    return (render_template("new-note.html"))

@chat.route("/new-chat/create")
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
@chat.route("/chat/getinfo/<chatid>")
def get_chat_info(chatid):
    cht_info = chats_coll.document(chatid)
    session[chatid] = False	
    return (jsonify(cht_info.get().to_dict()))


@chat.route("/chat/add/<chatid>/<message>")
def add_chat(chatid, message):

    chat_doc = chats_coll.document(chatid)
    chat_details = chat_doc.get().to_dict()
    chat_details["chat"] += "\n[{}] : {}".format(session.get("email_addr").split("@")[0], message)
    chat_doc.update(chat_details, option=None)

    # need to handle errors but for now
    return (jsonify({}))

@chat.route("/chat/leave/<chatid>")
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

@chat.route("/chat/<chatid>")
def user_chat(chatid):
    '''
        TODO: Hacer ventana de chats como la de cualquier app de mensajeo con los profesores registrados y alumnos.
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

        # Trying to implement users connected chats list            
        user_doc = users_coll.document(session['id'])
        user_details = user_doc.get().to_dict()
        connected_chats = user_details.get("connected_chats")
        session["user_name"] = user_details.get("name")
        #flash(decoded_clamis)

        connected_chats_list = []
        for i in connected_chats:
            connected_chats_list.append(i.get().to_dict())

        return (render_template("chat.html", users_list=chat_details.get("users"), logged_user=session["email_addr"], chatid=chatid, user_email = session["email_addr"],active=4, chats_list=connected_chats_list[::-1],profileid=session["about_file_ID"]))
    except Exception as e:
        return str(e)
