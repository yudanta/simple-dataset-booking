#!/usr/bin/env python 
import os 
import sys 

from os import path 
from datetime import datetime, timedelta

APP_NAME = 'Dataset Booking Management'
BASE_URL = ''
APP_URL = ''
BASEDIR = os.path.abspath(os.path.dirname(__file__))
# DEBUG
DEBUG = True 

SECRET_KEY = 'ca2b84ac72a91a20cbda828a2be2d1f2c1fb7521'

secure_scheme_headers = {'X-FORWARDED-PROTOCOL': 'ssl', 'X-FORWARDED-PROTO': 'https', 'X-FORWARDED-SSL': 'on'}

# SQLALCHEMY CONFIG
SQLALCHEMY_DATABASE_URI = 'sqlite://murakami_test.db'
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# Flask-Login 
REMEMBER_COOKIE_DURATION = 1 # n-days 

DATASETS_BASE_PATH = '/contentfiles/datasets/'