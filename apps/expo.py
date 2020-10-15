from init import *


expoBP = Blueprint('expoBP',__name__)



def GetPosts(sortby = 'rt_OgRetwCount',limit=50):	   
	# TODO
	pass



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


