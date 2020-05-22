import os
from sqlalchemy import Column, String, Integer, create_engine,DateTime
from flask_sqlalchemy import SQLAlchemy
import json
# from flask_migrate import Migrate

database_name = "moviesdb"
database_path = "postgres://{}/{}".format('localhost:5433', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5433/moviesdb'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    #migrate = Migrate(app,db)
    db.init_app(app)
    db.create_all()
    return db

    
# Movie model

class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    release_date = db.Column(db.String())

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date':self.release_date
        }

#Actor model
class Actor(db.Model):
    __tablename__='actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer)
    gender = db.Column(db.String())
    
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender':self.gender
        }

#this is the association table as the relation here is many to many
class Association(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)
    def __init__(self, movie_id, actor_id):
        self.actor_id = actor_id
        self.movie_id = movie_id
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()