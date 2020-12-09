#!/usr/bin/env python 
from app import app, migrate, manager 
from app import SqlDB as db 
from app.helpers.hashhelper import HashHelper
from app.models import Users

def seed_users():
    # seed users 
    watson = Users()
    watson.username = 'watson'
    watson.password = HashHelper().generate_bcrypt_hash('098321')
    watson.email = 'watson@datasetman.local'
    watson.firstname = 'Watson'
    watson.status = 1

    haruki = Users()
    haruki.username = 'haruki'
    haruki.password = HashHelper().generate_bcrypt_hash('098321')
    haruki.email = 'haruki@datasetman.local'
    haruki.firstname = 'Haruki'
    haruki.status = 1

    adler = Users()
    adler.username = 'adler'
    adler.password = HashHelper().generate_bcrypt_hash('098321')
    adler.email = 'adler@datasetman.local'
    adler.firstname = 'Adler'
    adler.status = 1

    brown = Users()
    brown.username = 'brown'
    brown.password = HashHelper().generate_bcrypt_hash('098321')
    brown.email = 'brown@datasetman.local'
    brown.firstname = 'Brown'
    brown.status = 1

    # insert user 
    for user in [watson, haruki, adler, brown]:
        try:
            db.session.add(user)
            db.session.commit()
            print('success seed new user: {}'.format(user.username))
        except Exception as e:
            print(e)
            db.session.rollback()
    