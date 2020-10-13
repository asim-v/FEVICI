from init import *


expoBP = Blueprint('expoBP',__name__)


@expoBP.route("/expo")
def expo():
    return render_template("expo.html",user_name=session["user_name"],status = session['status'],active=6,profileid=session["about_file_ID"])
