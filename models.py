from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import os
import json

database_path = 'postgres://xuaxhwzdrjnqhl:ee73d75462b8fd47af1657ba6c901a26cf1ae8b1ab35ea0d7bf88b24f94deb49@ec2-184-72-235-159.compute-1.amazonaws.com:5432/d4196ei3odppte'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String)
    age = Column(Integer)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
