from init import *


calendarBP = Blueprint('calendarBP',__name__)



@calendarBP.route("/calendar")
def calendar():
    return render_template("calendar.html",user_name=session["user_name"],status = session['status'],active=3,profileid=session["about_file_ID"])
