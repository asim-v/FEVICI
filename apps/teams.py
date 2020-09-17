from flask import Blueprint
from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify,send_from_directory

teams = Blueprint('teams',__name__)



@teams.route("/recieve_invite/<invite_id>")
def recieve_invite(invite_id):
    '''
        TODO: Dos opciones de invitación:
            1) El usuario recibe un correo y es redirigido al about donde se muestra el código de invitación recibido
            2) El usuario utiliza el cógido de invitación que también se muestra en el popup de project para ingtesarlo manualmente 
    '''
    pass



@teams.route("/send_invite/<invite_to>")
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

class team(object):
    def __init__(self,id):
        self.doc = user_doc = users_coll.document(id)
        self.name = user_doc.get().to_dict().get("name")
        self.email = user_doc.get().to_dict().get("email")
        self.color = random.choice(["#6772E5","#D869D0","#FF71A6","#FF967B","#FFC761"])
        self.initials = ''.join([x[0].upper() for x in self.name.split(' ')][:3])
