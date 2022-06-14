from flask import Flask, jsonify,request,session,redirect,url_for
from flask_cors import CORS
# from models import *
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
# from flask_socketio import SocketIO, send,join_room,leave_room
# from flask_mail import Mail, Message as Msg
# from api import api
# from admin import admin
from config import ProductionConfig
app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins='*')

CORS(app) 
# db.init_app(app)
# app.config['SECRET_KEY'] = "kjsgjgfdskhgfdskhgfksgkfqgkfq"
# # app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://cwzwxlcnxuuxcn:b3587ceac71fde4de7702940eca4b62bbe95a0394f29d3898303d3a3f17cd71c@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/d814n28lilrokf"
# app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///test.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'sepanouir.amdin@gmail.com'
# app.config['MAIL_PASSWORD'] = 'devpro2022'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# config=ProductionConfig()
# if env:
# 	app.config.from_object(DeveloppementConfig)
# else:
app.config.from_object(ProductionConfig)

# app.register_blueprint(api)
# admin.init_app(app)


@app.route('/',methods=['GET'])
def get_all_users():
	return jsonify({"message":"hello"})
# mail = Mail(app)

# @app.route('/send_email/<email>/<nbr>',methods=['GET'])
# def send_email(email,nbr):
# 	# try :
# 	msg = Msg('Confirm Email', sender='sepanouir.admin@gmail.com', recipients=[email])
# 	msg.body = f"L'application sepanouir vous demande un code de verification qu'est '{nbr}' ."
# 	mail.send(msg)
# 	return jsonify({"message":"send"})
	# except Exception as e:
	# 	return jsonify({"message":"error"})

# @socketio.on('message')
# def handleMessage(data):
# 	new_msg = Message(
# 			user_id=User.getUser(data['user_id']).id, 
# 			room_id=data['room_id'], 
# 			msg=data['msg']
# 		    )
# 	Us = [User.query.filter_by(id=i.user_id).first().public_id for i in Participants.query.filter_by(room_id=data['room_id']).all()]
# 	print(Us)
# 	db.session.add(new_msg)
# 	db.session.commit()
# 	if str(Us[0])==str(data['user_id']):
# 		send({"user1":str(Us[0]),"user2":str(Us[1])},broadcast=True)
# 	else:
# 		send({"user1":str(Us[1]),"user2":str(Us[0])},broadcast=True)

# @app.route("/login",methods=['POST'])
# def login():
# 	email=request.form['email']
# 	password=request.form['password']
# 	print(f'email :{email} \nPassword :{password}')
# 	# print(request.form)
# 	session['admin']=True
# 	return redirect(admin.url)


# @socketio.on('message',namespace='/comment')
# def post_user_partenaire(data):
# 	new_comment = Partenaire_user(
# 		user_id=User.getUser(data['user_id']).id, 
# 		partenaire_id=data['partenaire_id'], 
# 		comment=data['comment']
# 	    )
# 	db.session.add(new_comment)
# 	db.session.commit()
# 	send("refresh comment",broadcast=True)


if __name__ == '__main__':
	# socketio.run(app,debug=True)
	app.run(debug=True)
	# kkjsdhjkfhsdkjhfjksd
# web: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 app:app
