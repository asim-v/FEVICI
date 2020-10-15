from init import *


indexBP = Blueprint('indexBP',__name__)


@indexBP.route('/')
def index_page():
    '''
        Pagina de inicio
    '''
    flash_msg = None
    if "session_id" in session:
        try:
            # verify session_id
            decoded_clamis = auth.verify_session_cookie(session["session_id"])   
            #flash(decoded_clamis)
            session['email_addr'] = decoded_clamis['email']
            session['id'] = decoded_clamis['user_id']
            #session variable to indicate errors
            session["status"]  = None
            

            # Trying to implement users connected chats list            
            user_doc = users_coll.document(session['id'])
            user_details = user_doc.get().to_dict()
            session["user_name"] = user_details.get("name")
            #flash(decoded_clamis)
            
            session['about_file_ID'] = user_details["about_file"]["image_id"]

            return render_template("index.html", user_email=session["email_addr"],user_name=session["user_name"],active=1,profileid=session["about_file_ID"])
        except Exception as e:
            # if unable to verify session_id for any reason
            # maybe invalid or expired, redirect to login
            flash_msg = "Your session is expired!"
            #return "INDEX EXCEPTION" + str(e)
            return redirect(url_for("loginBP.user_login"))    

    flash_msg = "Please Log In"
    flash(flash_msg)
    return redirect(url_for("loginBP.user_login"))    
