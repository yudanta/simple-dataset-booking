#!/usr/bin/env python 
from functools import wraps 
from flask import g, request, redirect, url_for, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required 

from app import app, SqlDB as db 