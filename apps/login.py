from init import *



loginBP = Blueprint('loginBP',__name__)



@loginBP.route('/login', methods=["GET","POST"])
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
            return redirect(url_for('indexBP.index_page'))

        except requests.HTTPError as e:
            if ("EMAIL_NOT_FOUND" in str(e)):
                flash_msg = "Favor de registrarse antes de ingresar"
            elif ("INVALID_EMAIL" in str(e)):
                flash_msg = "Por favor ingresa un correo válido"
            elif ("INVALID_PASSWORD" in str(e)):
                flash_msg = "Contraseña inválida"
            else:
                flash_msg = "Algo salio mal!!" + str(e)
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

    return render_template("login.html",auth = False)
    

@loginBP.route('/logout')
def user_logout():
    session.pop('session_id', None)
    session.clear()
    return redirect(url_for('indexBP.index_page'))
