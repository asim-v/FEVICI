from init import *


expoBP = Blueprint('expoBP',__name__)


def GetTweet(id):	   
	'''
		Obtiene tweet de la bd y actualiza el texto con el contenido completo
	'''

	# Importa database module.	
	data = db.reference("extraction").order_by_child("tw_id_str").equal_to(id).limit_to_first(1).get()

	# Parsea JSON en un objeto correspondiente por cada keys del dict.
	def json2obj(x,show = False): 		

		#twitter.com/anyuser/status/541278904204668929

		def _json_object_hook(d): return namedtuple("tweet", d.keys())(*d.values())
		data = str(dict(x)[list(x.keys())[0]])
		data = str(data).replace(': False',': "False"').replace(': True',': "True"').replace("'",'"')

		if show == True: print(json.dumps(x, indent=4, sort_keys=True))
		return json.loads(data, object_hook=_json_object_hook)
	try:
		return dict(data)[list(data.keys())[0]]
	except Exception as e:
		return e
	#print(type(snapshot[post]),snapshot[post],json2obj(snapshot[post]))


def GetPosts(sortby = 'rt_OgRetwCount',limit=50):	   
	
	# Importa database module.	
	ref = db.reference('extraction') #Establece ref a grupo de posts
	snapshot = ref.order_by_child(sortby).limit_to_last(limit).get()  #Posts más retwiteados	
	
	# Parsea JSON en un objeto correspondiente por cada keys del dict.

	def _json_object_hook(d): return namedtuple("tweet", d.keys())(*d.values())
	def json2obj(x): 
		data = str(x).replace('False','"False"').replace('True','"True"').replace("'",'"')
		return json.loads(data, object_hook=_json_object_hook)
	for post in snapshot:
		#print(json.dumps(snapshot[post], indent=4, sort_keys=True))	#PrettyPrint
		try:total_posts.append(json2obj(snapshot[post]))
		except:pass#print(type(snapshot[post]),snapshot[post],json2obj(snapshot[post]))
	return (total_posts[::-1],snapshot) #Obtiene la lista de objetos y el json




@expoBP.route("/expo")
def expo():
    return render_template("expo.html",user_name=session["user_name"],status = session['status'],active=6,profileid=session["about_file_ID"])

@expoBP.route("/get/<cat>/<num>",methods=["POST"])
def get(cat,num):
	num = int(num)
	if request.method == "POST":

		if cat=='random':
			response = {}
			for i in users_coll.order_by(u"project_desc").limit(num).get():
				res = {}
				dictionary = i.to_dict()
				for key in dictionary.keys():
					if key != 'connected_chats':
						res[key] = dictionary[key]															
					
				if len(res.keys()) > 0:
					response[i.id] = res	

			return jsonify(response)
			
		if cat=='category':
			return jsonify([x.to_dict() for x in users_coll.order_by(u"project_desc.Category").limit(num).get()])

		if cat=='subcategory':
			return jsonify([x.to_dict() for x in users_coll.order_by(u"project_desc.Subcategory").limit(num).get()])


