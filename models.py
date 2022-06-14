from sqlalchemy_utils import UUIDType
from flask_sqlalchemy import SQLAlchemy
import datetime
import uuid

db=SQLAlchemy()


Activite_user = db.Table('activite_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('activite_id', db.Integer, db.ForeignKey('activity.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    public_id = db.Column(UUIDType(binary=False),default=uuid.uuid1,unique=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    sexe = db.Column(db.String(50))
    date_naissance = db.Column(db.Date)
    ville_residence = db.Column(db.String(50),nullable=False)
    medecin_traitant = db.Column(db.String(50))
    metier = db.Column(db.String(50))
    debut_SEP = db.Column(db.Integer)
    loisirs = db.Column(db.String(50))
    email = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(80),nullable=False)
    auth = db.Column(db.Boolean)
    activities = db.relationship('Activity', secondary=Activite_user, lazy='subquery',backref=db.backref('users', lazy=True))
    comments = db.relationship('Partenaire_user', backref='user', lazy=True)
    activities_attend = db.relationship('activite_user_attend', backref='user', lazy=True)
    particpants = db.relationship('Participants', backref='user', lazy=True)
    msgs = db.relationship('Message', backref='user', lazy=True)
    def __repr__(self):
        return 'Utilisateur %r' % self.email
    @staticmethod
    def getUser(public_id):
        return User.query.filter_by(public_id=public_id).first()

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    public_id = db.Column(UUIDType(binary=False),default=uuid.uuid1,unique=True)
    name = db.Column(db.String(50))
    members = db.Column(db.Integer)
    img = db.Column(db.Text)
    date = db.Column(db.Date)
    details = db.Column(db.Text)
    activities_attend = db.relationship('activite_user_attend', backref='activity', lazy=True)

    def __repr__(self):
        return 'Activité %r' % self.name
    @staticmethod
    def getActivity(public_id):
        return Activity.query.filter_by(public_id=public_id).first()
class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    titre = db.Column(db.String(50))
    details = db.Column(db.Text)
    img = db.Column(db.Text)
    url = db.Column(db.Text)


class Alimentation(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    titre = db.Column(db.String(50))
    details = db.Column(db.Text)

class Partenaire(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String(50))
    ville = db.Column(db.String(50))
    img = db.Column(db.Text)
    comments = db.relationship('Partenaire_user', backref='partenaire', lazy=True)

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nom = db.Column(db.String(50))
    img = db.Column(db.Text)

class Partenaire_user(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    partenaire_id = db.Column(db.Integer, db.ForeignKey('partenaire.id'),nullable=False)
    comment=db.Column(db.Text,nullable=False)


# class user_contact(db.Model):
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
#     sender_id = db.Column(db.Integer, db.ForeignKey('partenaire.id'),nullable=False)


class became_Partenaire(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(50))
    details = db.Column(db.Text)

class activite_user_attend(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'),nullable=False)


class Options(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    about = db.Column(db.Text)
    donation = db.Column(db.Text)
    qui_somme_nous = db.Column(db.Text)
    sEP_c_est_quoi = db.Column(db.Text)
    mot_de_presidente = db.Column(db.Text)
    rIB = db.Column(db.String(80))

class Participants(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'),nullable=False)
    def __repr__(self):
        return f'Part {self.user_id}: Room :{self.room_id}'

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    particpants = db.relationship('Participants', backref='room', lazy=True)
    msgs = db.relationship('Message', backref='room', lazy=True)
    room=db.Column(db.String(50),nullable=False,unique=True)
    def __repr__(self):
        return 'Utilisateur %r' % self.room

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'),nullable=False)
    msg = db.Column(db.Text)
    viewed = db.Column(db.Boolean)
    time = db.Column(db.DateTime,default=datetime.datetime.now)

