from flask import Flask
import sqlite3, datetime, os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from . import db_manager as db

app = Flask(__name__)

# ruta absoluta d'aquesta carpeta
basedir = os.path.abspath(os.path.dirname(__file__)) 

# paràmetre que farà servir SQLAlchemy per a connectar-se
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir + "/database.db"
# mostre als logs les ordres SQL que s'executen
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy()
db.init_app(app)
now = datetime.datetime.utcnow

class categoria(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, nullable=False)

class product(db.Model):
    __tablename__ = "products"
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title           = db.Column(db.Text, nullable=False)
    description     = db.Column(db.Text, nullable=False)
    photo           = db.Column(db.Text, nullable=False)
    price           = db.Column(db.Numeric(10,2), nullable=False)
    category_id     = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    seller_id       = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created         = db.Column(db.DateTime, default=now)
    updated         = db.Column(db.DateTime, default=now)


# taula users

class user(db.Model):
    __tablename__   = "users"
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name            = db.Column(db.Text, nullable=False, unique=True)
    email           = db.Column(db.Text, nullable=False, unique=True)
    password        = db.Column(db.Text, nullable=False)
    created         = db.Column(db.DateTime, default=now)
    update          = db.Column(db.DateTime, default=now)
