#!/usr/bin/env python 
from flask import Blueprint, request, render_template
from flask_login import login_user, logout_user, current_user, login_required 
from app.helpers.getuser import get_user

from app.models import Users, Datasets, BookDatasets

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/')
@login_required
def index():
    logged_in_user = get_user(current_user)

    data = {
        'logged_in_user': logged_in_user,
        'active_users': 0,
        'active_datasets': 0,
        'active_task_booking': 0,
    }

    # stats data 
    data['active_users'] = Users.query.filter(Users.status==1).count()
    data['active_datasets'] = Datasets.query.filter(Datasets.status==1).count()
    data['active_task_booking'] = BookDatasets.query.filter(BookDatasets.is_deleted==0).count()


    return render_template('cms/dashboard/index.html', data=data)