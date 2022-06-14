from models import Activity,db,User,Activite_user,Sport,Alimentation,Partenaire,Partenaire_user,Options,became_Partenaire,Sponsor,activite_user_attend,Participants,Room,Message
from flask import request,Blueprint,jsonify
import datetime
import jwt
from config import ProductionConfig
SECRET_KEY=ProductionConfig.SECRET_KEY
from functools import wraps

api=Blueprint('api','__name__',url_prefix='/api')
#,template_folder='templates/views')


#  ------------------ functools -----------------------

def conv(o):
	return "{}-{}-{}".format(o.year, o.month, o.day)
 
def conv_(o):
	T=[int(i) for i in o.split("-")]
	print(T)
	return datetime.date(T[0], T[1], T[2])


def inter(R,T):
	out=[]
	print(R)
	print(T)
	for r in R:
		if r in T:
			out.append(r)
	if len(out)==0:
		return 0
	return out[0]

def Try(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		try:
			return f(*args, **kwargs)
		except Exception as e:
			return jsonify([])
	return wrapper

def token_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			return jsonify({'message' : 'Token is missing!'}), 401

		try: 

			print(token)
			data = jwt.decode(token,SECRET_KEY, algorithms=["HS256"])
			# current_user = User.query.filter_by(public_id=data['public_id']).first()
		except:
			return jsonify({'message' : 'Token is invalid!'}), 401

		# return f(current_user, *args, **kwargs)
		return Try(f(*args, **kwargs))

	return wrapper






# @api.route('/activity',methods=['GET'])
# def get_activity():
# 	try:
# 		acts = Activity.query.all()
# 		output = [{
# 		'id': str(act.id),
# 		"name":act.name, 
# 		"members":act.members, 
# 		"img":act.img, 
# 		"date": conv(act.date), 
# 		"details":act.details,
# 		"members_disp":act.members-len(act.users)
# 		} 
# 		for act in acts]
# 		return jsonify(output)
# 	except:
# 		return jsonify({'message': 'error'})

@api.route('/test_token',methods=['GET'])
@token_required
def test_token():
	return jsonify({"message":"test is valid !!!!!!!"})




@api.route('/users/<string:email>/<string:password>',methods=['GET'])
@Try
def get_user(email,password):
	# try:
	user = User.query.filter_by(email=email,password=password).first()
	print(user)
	token = jwt.encode({'id' : str(user.public_id), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1)}, SECRET_KEY, algorithm="HS256")
	return jsonify({
	"id":str(user.public_id),
	"nom":user.nom, 
	"prenom":user.prenom, 
	"sexe":user.sexe, 
	"date_naissance":conv(user.date_naissance), 
	"ville_residence":user.ville_residence, 
	"medecin_traitant":user.medecin_traitant, 
	"metier":user.metier, 
	"debut_SEP":user.debut_SEP, 
	"loisirs":user.loisirs, 
	"email":user.email, 
	"password":user.password, 
	"auth":user.auth, 
	"token":token		
	})
	# except Exception as e:
	# 	return jsonify({"message":"error"})
@api.route('/check_email/<string:email>',methods=['GET'])
@Try
def check_email(email):
	# try:	
	user = User.query.filter_by(email=email).first()
	if user :
		return jsonify({"message":1})
	return jsonify({"message":0})
	# except Exception as e:
	# 	return jsonify({"message":"error"})
@api.route('/users/<id>',methods=['GET'])
@token_required
def get_user_by_id(id):
	# try:
	user = User.query.filter_by(public_id=id).first()
	return jsonify({
	"id":str(user.public_id),
	"nom":user.nom, 
	"prenom":user.prenom, 
	"sexe":user.sexe, 
	"date_naissance":conv(user.date_naissance), 
	"ville_residence":user.ville_residence, 
	"medecin_traitant":user.medecin_traitant, 
	"metier":user.metier, 
	"debut_SEP":user.debut_SEP, 
	"loisirs":user.loisirs, 
	"email":user.email, 
	"password":user.password, 
	"auth":user.auth, 		
})
	# except Exception as e:
	# 	return jsonify({"message":"error"})


@api.route('/users',methods=['POST'])
def post_users():
	# try:
	data = request.get_json(force=True)
	new_user = User(
		nom=data['nom'], 
		prenom=data['prenom'], 
		sexe=data['sexe'], 
		date_naissance=conv_(data['date_naissance']), 
		ville_residence=data['ville_residence'], 
		medecin_traitant=data['medecin_traitant'], 
		metier=data['metier'], 
		debut_SEP=data['debut_SEP'], 
		loisirs=data['loisirs'], 
		email=data['email'], 
		password=data['password'], 
		auth=data['auth'], 
	    )
	db.session.add(new_user)
	db.session.commit()
	return jsonify({'message' : 'New user created!'})
	# except Exception as e:
		# return jsonify({"message":"error"})


@api.route('/all_users/<id>',methods=['GET'])
@Try
def get_all_users(id):
	users = User.query.filter_by().all()
	return jsonify([{
		"id":str(user.public_id),
		"nom":user.nom, 
		"prenom":user.prenom, 
		"sexe":user.sexe, 
		"date_naissance":conv(user.date_naissance), 
		"ville_residence":user.ville_residence, 
		"medecin_traitant":user.medecin_traitant, 
		"metier":user.metier, 
		"debut_SEP":user.debut_SEP, 
		"loisirs":user.loisirs, 
		"email":user.email, 
		"password":user.password, 
		"auth":user.auth,
		"room":inter(R=[R1.room_id for R1 in Participants.query.filter_by(user_id=User.getUser(id).id).all()], 
			T=[R2.room_id for R2 in Participants.query.filter_by(user_id=user.id).all()])
	} for  user in users if str(user.public_id)!=str(id)])

@api.route('/user_activity/<string:user_id>',methods=['GET'])
@token_required
def get_user_activity(user_id):
	# try:
	activities = User.getUser(user_id).activities
	output = [{
	'id': str(act.public_id),
	"name":act.name, 
	"members":act.members, 
	"img":act.img, 
	"date": conv(act.date), 
	"details":act.details,
	"members_disp":act.members-len(act.users)
	} 
	for act in activities]
	output.reverse()
	return jsonify(output)
	# except Exception as e:
	# 	return jsonify([])	

@api.route('/user_activity/other/<string:user_id>',methods=['GET'])
@Try
def get_user_activity_other(user_id):
	# try:	
	if str(user_id) == "0":
		activities =Activity.query.order_by(Activity.id.desc()).all()
		output = [{
		'id': str(act.public_id),
		"name":act.name, 
		"members":act.members, 
		"img":act.img, 
		"date": conv(act.date), 
		"details":act.details,
		"members_disp":0
		} 
		for act in activities]
		return jsonify(output)
	user_id=User.getUser(user_id).id
	act = User.query.filter_by(id=user_id).first().activities
	act_att =[Activity.query.filter_by(id=i.activity_id).first() for i in activite_user_attend.query.filter_by(user_id=user_id).all()]
	activities =[i for i in Activity.query.order_by(Activity.id.desc()).all() if (not( i in act) and not(i in act_att))]
	output = [{
	'id': str(act.public_id),
	"name":act.name, 
	"members":act.members, 
	"img":act.img, 
	"date": conv(act.date), 
	"details":act.details,
	"members_disp":act.members-len(act.users)
	} 
	for act in activities]
	return jsonify(output)
	# except Exception as e:
	# 	return jsonify([])	

@api.route('/user_activity',methods=['POST'])
@token_required
def post_user_activity():
	data = request.get_json(force=True)		
	print(data)
	# try:
	# activity=Activity.query.filter_by(id=activity_id).first()
	activity=Activity.getActivity(data['activity_id'])
	# user = User.query.filter_by(id=user_id).first()
	user = User.getUser(data['user_id'])
	l=activity.members-len(activity.users)
	if l > 0 :
		user.activities.append(activity)
		db.session.commit()
		return jsonify({"message":"seccus"})
	return jsonify({"message":"error"})
	# except Exception as e:
	# 	return jsonify({"message":"error"})



@api.route('/user_activity/<string:user_id>/<string:activity_id>',methods=['DELETE'])
@token_required
def delete(user_id,activity_id):
	# try:
	# activity=Activity.query.filter_by(id=activity_id).first()
	activity=Activity.getActivity(public_id=activity_id)
	# user = User.query.filter_by(id=user_id).first()
	user = User.getUser(user_id)
	user.activities.remove(activity)
	try:
		New_user=activite_user_attend.query.filter_by(activity_id=activity.id).first()
		A=User.query.filter_by(id=New_user.user_id).first()
		A.activities.append(activity)
		db.session.delete(New_user)
	except Exception as e:
		pass
	db.session.commit()
	return jsonify({"message":"seccus"})
	# except Exception as e:
	# 	return jsonify({"message":"error"})


@api.route('/sport',methods=['GET'])
@Try
def get_all_sports():
	# try:
	sports = Sport.query.all()
	output = [{
	'id': sport.id,
	"titre":sport.titre, 
	"details":sport.details, 
	"img":sport.img, 
	"url":sport.url
	} 
	for sport in sports]
	return jsonify(output)
	# except Exception as e:
	# 	return jsonify([])

@api.route('/alimentation',methods=['GET'])
@Try
def get_all_Alimentations():
	Alimentations = Alimentation.query.all()
	# try:
	output = [{
	'id': Alimentation.id,
	"titre":Alimentation.titre, 
	"details":Alimentation.details, 
	} 
	for Alimentation in Alimentations]
	return jsonify(output)
	# except Exception as e:
	# 	return jsonify([])

@api.route('/partenaire',methods=['GET'])
@Try
def get_all_Partenaires():
	Partenaires = Partenaire.query.all()
	# try :
	output = [{
	'id': str(Partenaire.id),
	"nom":Partenaire.nom, 
	"ville":Partenaire.ville, 
	"img":Partenaire.img, 
	"comments":len(Partenaire.comments)
	} 
	for Partenaire in Partenaires]
	return jsonify(output)
	# except Exception as e:
	# 	return jsonify([])

@api.route('/partenaire/<string:id>',methods=['GET'])
@token_required
def get_Partenaires_comments(id):
	partenaire = Partenaire.query.filter_by(id=id).first()
# try:
	T=[]
	for comment in partenaire.comments:
		user=User.query.filter_by(id=comment.user_id).first()
		T.append({
	'id': comment.id,
	"user_name":user.nom+" "+user.prenom, 
	"user_id":str(user.public_id),
	"comment":comment.comment
	} )
	return jsonify(T)
	# except Exception as e:
	# 	return jsonify({"message":"error"})

@api.route('/sponsor',methods=['GET'])
@Try
def post_sponsor():
	sponsors=Sponsor.query.all()
	# try:
	return jsonify([{
		'nom':sponsor.nom,
		'img':sponsor.img
		} for sponsor in sponsors])
	# except Exception as e:
	# 	return jsonify({"message":"error"})	

@api.route('/partenaire_user',methods=['POST'])
@token_required
def post_user_partenaire():
	# try:
	data = request.get_json(force=True)
	new_comment = Partenaire_user(
		user_id=User.getUser(data['user_id']).id, 
		partenaire_id=data['partenaire_id'], 
		comment=data['comment']
	    )
	db.session.add(new_comment)
	db.session.commit()
	return jsonify({'message' : 'New comment created!'})
	# except Exception as e:
	# 	return jsonify({"message":"error"})	

@api.route('/became_partenaire',methods=['POST'])
@token_required
def became_partenaire_():
	# try:
	data = request.get_json(force=True)
	new_partnr = became_Partenaire(
		email=data['email'], 
		details=data['details'] 
	    )
	db.session.add(new_partnr)
	db.session.commit()
	return jsonify({'message' : 'New prtnr created!'})
	# except Exception as e:
	# 	return jsonify({"message":"error"})	

@api.route('/options',methods=['GET'])
@Try
def Options_():
	option = Options.query.first()
	# try:
	output = {
	"about":option.about, 
	"donation":option.donation, 
	"qui_somme_nous":option.qui_somme_nous, 
	"sEP_c_est_quoi":option.sEP_c_est_quoi, 
	"mot_de_presidente":option.mot_de_presidente, 
	"rIB":option.rIB, 
	} 
	return jsonify(output)
	# except Exception as e:
	# 	return jsonify({"message":"error"})


@api.route('/activite_user_attend',methods=['POST'])
@token_required
def activite_user_attend_():
	# try:
	data = request.get_json(force=True)
	# user_id=data['user_id']
	user_id=User.getUser(data['user_id']).id

	# activity_id=data['activity_id']
	activity_id=Activity.getActivity(data['activity_id']).id

	new_user = activite_user_attend(
		user_id=int(user_id), 
		activity_id=int(activity_id)
	    )
	db.session.add(new_user)
	db.session.commit()
	return jsonify({'message' : 'New activite_user_attend created!'})
	# except Exception as e:
	# 	return jsonify({"message":"error"})	

@api.route('/activite_user_attend/<string:user_id>/<string:activity_id>',methods=['DELETE'])
@token_required
def activite_user_attend_delete(user_id,activity_id):
	# try:
	user_id=User.getUser(user_id).id
	activity_id=Activity.getActivity(activity_id).id
	au = activite_user_attend.query.filter_by(user_id=user_id, activity_id=activity_id).first()
	db.session.delete(au)
	db.session.commit()
	return jsonify({'message' : 'activite_user_attend deleted!'})
	# except Exception as e:
	# 	return jsonify({"message":"error"})	

@api.route('/activite_user_attend/<string:user_id>',methods=['GET'])
@token_required
def activite_user_attend_get(user_id):
	# try:
	user_id=User.getUser(user_id).id
	acts_id = [i.activity_id for i in  activite_user_attend.query.filter_by(user_id=user_id).all()]
	

	acts = [Activity.query.filter_by(id=i).first() for i in acts_id]
	output = [{
	'id': str(act.public_id),
	"name":act.name, 
	"members":act.members, 
	"img":act.img, 
	"date": conv(act.date), 
	"details":act.details,
	"members_rest":[i.user_id for i in activite_user_attend.query.filter_by(activity_id=act.id).all()].index(int(user_id)),
	} 
	for act in acts]
	return jsonify(output)
	# except:
	# 	return jsonify([])

# @api.route('/user_contact/<string:user_id>',methods=['GET'])
# def user_contact_id(user_id):
# 	try:
# 		users =User.query.filter_by(id=user_id).all
# 		return jsonify([{'id': str(user.id)} for user in users])

# 	except Exception as e:
# 		return jsonify({"message":"error"})

@api.route('/contacts/<uid>',methods=["GET"])
@token_required
def get_contacts(uid=1):
	# try:
	uid=User.getUser(uid).id
	Rooms=Participants.query.filter_by(user_id=uid).all()
	contacts =[[P for P in  Participants.query.filter_by(room_id=R.room_id) if P.user_id!=uid][0] for R in Rooms]
	last_msgs=[Message.query.filter_by(room_id=R.room_id).order_by(Message.id.desc()).first().msg for R in contacts]
	output=[{
		"room_id":Rooms[i].room_id,
		"user_name":User.query.filter_by(id=contacts[i].user_id).first().email,
		"last_msg":last_msgs[i],
	} for i in range(len(Rooms))]
	return jsonify(output)
	# except Exception as e:
	# 	return jsonify([])
# Message.id.desc()
@api.route('/add_message',methods=['POST'])
@token_required
def add_msg():
	# try:
	data = request.get_json(force=True)
	user_id=User.getUser(data['user_id']).id
	new_msg = Message(
		user_id=user_id, 
		room_id=data['room_id'], 
		msg=data['msg']
	    )
	db.session.add(new_msg)
	db.session.commit()
	return jsonify({'message' : 'New message created!'})
	# except Exception as e:
	# 	return jsonify({"message":"error"})

@api.route('/add_room',methods=['POST'])
@token_required
def add_room():
	# try:
	data = request.get_json(force=True)
	user_id=User.getUser(data['user_id']).id
	uid=User.getUser(data['uid']).id
	check_room=inter(R=[R1.room_id for R1 in Participants.query.filter_by(user_id=user_id).all()], 
		T=[R2.room_id for R2 in Participants.query.filter_by(user_id=uid).all()])
	if check_room !=0:
		return jsonify({'room' : check_room})
	R=Room(room=f"room{user_id}-{uid}")
	db.session.add(R)
	db.session.commit()
	db.session.add(Participants(user_id=user_id,room_id=R.id))
	db.session.add(Participants(user_id=uid,room_id=R.id))
	db.session.commit()
	return jsonify({'room' : R.id})
	# except Exception as e:
	# 	return jsonify({"message":"error"})



@api.route('/messages/<room_id>/<user_id>',methods=['GET'])
@token_required
def messages_room(room_id=1,user_id=1):
	# try:
	user_id=User.getUser(user_id).id
	M=Message.query.filter_by(room_id=room_id).all()
	for ms in M:
		if ms.user_id!=int(user_id):
			print(f"{ms.user_id}!={user_id}")
			ms.viewed=True
	db.session.commit()
	M=Message.query.filter_by(room_id=room_id).order_by(Message.id).all()
	return jsonify([{
			"name":User.query.filter_by(id=msge.user_id).first().prenom,
			"side" : 1 if msge.user_id==int(user_id) else 0,
			"message": msge.msg,
			"viewed":msge.viewed,
			"time":f"{msge.time.year}-{msge.time.month}-{msge.time.day} {msge.time.hour}:{msge.time.minute}"
	
		} for msge in M])
	# except Exception as e:
	# 	return jsonify([])