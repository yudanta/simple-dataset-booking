#!/usr/bin/env python 
from datetime import datetime
from app import app, SqlDB as db

from sqlalchemy.dialects.sqlite import SMALLINT 

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(255), unique=True)
    firstname = db.Column(db.String(100), default="")
    lastname = db.Column(db.String(100), default="")
    last_login_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)
    status = db.Column(SMALLINT, default=0)

    def __repr__(self):
        return self.username

	# Flask-Login integration
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return True
        
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return self.id


class Datasets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashcode = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    original_file_name = db.Column(db.String(255), nullable=False)
    original_file_ext = db.Column(db.String(10))
    original_file_size = db.Column(db.Integer(), default=0)
    hashed_filename = db.Column(db.String(255), nullable=False)
    hashed_filepath = db.Column(db.String(255), nullable=False)
    status = db.Column(SMALLINT, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer)

    user = db.relationship('Users', backref='DatasetUser', lazy=True)

    # def __repr__(self):
    #     return self.name


class BookDatasets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    datasets_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))
    is_deleted = db.Column(SMALLINT, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)

    dataset = db.relationship('Datasets', backref=db.backref('parent', lazy='dynamic'))