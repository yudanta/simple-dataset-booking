#!/usr/bin/env python 
import string 
import random 

from app import app, bcrypt

class HashHelper():
    def __init__(self):
        return None 

    def generate_bcrypt_hash(self, plain):
        return bcrypt.generate_password_hash(plain).decode('utf-8')

    def check_bcrypt_hash(self, plain, hashed):
        return bcrypt.check_password_hash(str(hashed).encode('utf-8'), plain)