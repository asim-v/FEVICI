from init import *


teamsBP = Blueprint('teamsBP',__name__)



@teamsBP.route("/recieve_invite/<invite_id>")
def recieve_invite(invite_id):
    '''
        TODO: Dos opciones de invitación:
            1) El usuario recibe un correo y es redirigido al about donde se muestra el código de invitación recibido
            2) El usuario utiliza el cógido de invitación que también se muestra en el popup de project para ingtesarlo manualmente 
    '''
    pass



@teamsBP.route("/send_invite/<invite_to>")
def send_invite(invite_to):
	with teams.app_context():

		'''
		    La pagina genera un id de invitación que al ser usado por otro usuario, sobreescribe su proyecto con el id del proyecto con el del enviado
		'''
		invite_to = str(invite_to)
		# invite_to = str(invite_to)
		msg = Message("Sup Famille",
		                  sender=("Invitación a la Feria Virtual de Ciencias e Ingenierías","contacto@fevici.org"),
		                  recipients=[invite_to])
		# msg.recipients = ["you@example.com"]
		# msg.add_recipient("somebodyelse@example.com")
		# msg = Message("Hello",
		#               sender=("Me", "me@example.com"))

		# assert msg.sender == "Me <me@example.com>"
		try:
			print(invite_to)
			msg.body = "Probanding"
			msg.html = "<b>Holassss quisiera decirte que entiendo que es dificil pero que harás? Cuál es tu visión? Cómo llegas a esa visión?</b>"

			mail.send(msg)
			return 'sent'
		except Exception as e:
			return str(e)

