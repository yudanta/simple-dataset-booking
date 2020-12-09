#!/usr/bin/env python 
from datetime import datetime

from sqlalchemy import or_
from app import app, SqlDB as db 
from app.helpers.hashhelper import HashHelper
from app.models import Users

class AuthHelper():
    tag = ""
    messages = ""
    errors = ""

    def __init__(self):
        return None

    def login_user(self, username, password):
        user = Users.query.filter(or_(Users.username==username, Users.email==username)).first()
        if user:
            cek_hash = HashHelper().check_bcrypt_hash(password, user.password)
            if cek_hash:
                #update last login data
                user.last_login_at = datetime.now()
                db.session.commit()

                return user
            else:
                return False 

    # def update_user_login_data(self, userid, data={}):
    #     user = Users.query.get(userid)
    #     if user:
    #         if 'last_login_at' in data:
    #             user.last_login_at = data['last_login_at']

    #             db.session.commit()
                

