from init import *


teamsBP = Blueprint('teamsBP',__name__)


@teamsBP.route('/invite/<id>')
def invite(id):
	if request.method == "GET":
		pass
		#used by > 
			# mail
			# about

		#if has not logged in then go creates the account with the team		
		#if has logged in then makes the process just a gogo
	if request.method == "DELETE":
		pass
		#exits the team		
	if request.method == "DELETE":
		pass



@teamsBP.route("/send_invite/<invite_to>")
def send_invite(invite_to):		
	if request.method == "GET":
		'''
		    La pagina genera un id de invitación que al ser usado por otro usuario, sobreescribe su proyecto con el id del proyecto con el del enviado
		'''
		invite_to = str(invite_to)
		# invite_to = str(invite_to)
		msg = Message("Sup Famille",
		                  sender=("Invitación a la Feria Virtual de Ciencias e Ingenierías","scientista.noreply@gmail.com"),
		                  recipients=[invite_to])
		# msg.recipients = ["you@example.com"]
		# msg.add_recipient("somebodyelse@example.com")
		# msg = Message("Hello",
		#               sender=("Me", "me@example.com"))
		# assert msg.sender == "Me <me@examplse.com>"
		try:

			print(invite_to)
			msg.body = "Probanding"
			msg.html = "<b>Holassss quisiera decirte que entiendo que es dificil pero que harás? Cuál es tu visión? Cómo llegas a esa visión?</b>"

			mail.send(msg)
			return jsonify('sent')
		except Exception as e:
			return jsonify(str(e))
	