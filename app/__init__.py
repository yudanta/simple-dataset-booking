#!/usr/bin/env python 
import time 
import datetime
import colors

from rfc3339 import rfc3339
from flask import (
    Flask, Blueprint, render_template, send_from_directory, Response, make_response, session, request, g, 
    jsonify, flash, redirect, url_for
    )
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager 
from flask_login import login_user, logout_user, current_user, login_required

# APP Config
app = Flask(__name__, instance_relative_config=True)

# bcrypt 
bcrypt = Bcrypt(app)

# Allow CORS for api endpoint 
CORS(app, resources={r"/api/*": {"origins": "*"}} )

# custom logger 
@app.before_request
def start_timer():
    g.start = time.time()

@app.after_request
def log_request(response):
    if request.path == '/favicon.ico':
        return response

    elif request.path.startswith('/static'):
        return response

    now = time.time()
    duration = round(now - g.start, 5)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt, utc=True)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method, 'blue'),
        ('path', request.path, 'blue'),
        ('status', response.status_code, 'yellow'),
        ('duration', '{}s'.format(duration), 'green'),
        ('time', timestamp, 'magenta'),
        ('ip', ip, 'red'),
        ('host', host, 'red'),
        ('params', args, 'blue')
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id, 'yellow'))

    parts = []
    for name, value, color in log_params:
        part = colors.color("{}={}".format(name, value), fg=color)
        parts.append(part)

    line = " ".join(parts)

    app.logger.info(line)

    return response

# load config 
app.config.from_object('config')
app.config.from_pyfile('application.cfg', silent=True)

#bcrypt
bcrypt = Bcrypt(app)

#create mysql db object
SqlDB = SQLAlchemy(app)

#migration 
migrate = Migrate(app, SqlDB)

manager = Manager(app)
manager.add_command('SqlDB', MigrateCommand)

# set flask login as session manager 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# callback user decorator 
from app.models import Users
@login_manager.user_loader
def load_user(id):
	return Users.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
def index():
    # return 'eiits... {}'.format(app.config['APP_NAME'])
    return redirect(url_for('login'))
    

from app.web.auth.form import LoginForm
from app.helpers.auth import AuthHelper

# auth section 
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('_flashes', None)
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    else:
        formdata = LoginForm()
        if request.method == 'GET':
            return render_template('auth/login.html', form=formdata)
        elif request.method == 'POST':
            if formdata.validate_on_submit() == False:
                return render_template('auth/login.html', form=formdata)
            else:
                auth = AuthHelper()
                user = auth.login_user(formdata.username.data, formdata.password.data)
                if user:
                    login_user(user)
                    session.pop('_flashes', None)
                    return redirect(url_for('dashboard.index'))
                else:
                    flash('username or password incorrect', 'errors')
                    formdata.password.data = None 
                    return render_template('auth/login.html', form=formdata)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))

@app.route('/robots.txt', methods=['GET', 'POST'])
def static_robots():
    return send_from_directory(app.static_folder, filename='/'.join(['robots', request.path[1:]]))

# api blueprint 
# from app.api.v_0_1 import api_v_0_1
# from app.api.v_0_1 import api
# app.register_blueprint(api_v_0_1)

# app
from app.web.dashboard import dashboard
from app.web.datasets import datasets
from app.web.tasks import tasks

app.register_blueprint(dashboard)
app.register_blueprint(datasets)
app.register_blueprint(tasks)