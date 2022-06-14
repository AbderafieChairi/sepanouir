from app import app,db
from models import *
import datetime
def create_db():
	db.create_all(app=app)
	db.session.commit()

A=User(
	nom = "Chairi",
	prenom = "Abderafie",
	sexe = "Masculin",
	date_naissance = datetime.date(2000, 1, 1),
	ville_residence = "Rabat",
	medecin_traitant = "Med VI",
	metier = "Prof",
	debut_SEP = 2020,
	loisirs = "Sport",
	email = "abderafiechairi@gmail.com",
	password = "123465789",
	auth = True)
B=Activity(
	name = "First Activity",
    members = 3,
    img = "hhh",
    date = datetime.date(2022, 5, 1),
    details = "hhhhhhh"
	)

with app.app_context():
	db.session.add(A)
	db.session.add(B)
	db.session.commit()
