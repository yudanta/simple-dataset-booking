#!/usr/bin/env python 
from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
from flask_login import login_user, logout_user, current_user, login_required 
from app.helpers.getuser import get_user

from app import SqlDB
from app.models import Users, Datasets, BookDatasets

from app.web.tasks.form import AddNewBookingTask, Datasets, Users

tasks = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks.route('/')
@login_required
def index():
    logged_in_user = get_user(current_user)

    data = {
        'logged_in_user': logged_in_user
    }

    booked_datasets = BookDatasets.query.filter((BookDatasets.user_id==logged_in_user['id']) & (BookDatasets.is_deleted==0)).all()
    
    data['booked_datasets'] = booked_datasets
    
    return render_template('cms/tasks/index.html', data=data)

@tasks.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    logged_in_user = get_user(current_user)

    data = {
        'logged_in_user': logged_in_user
    }

    form = AddNewBookingTask()

    if form.validate_on_submit():
        # valid data
        for item in form.data['datasets']:
            print(item.id, item.name, item.description)
            # check if exists and status = 1, if not exist create new 
            check = BookDatasets.query.filter((BookDatasets.user_id==logged_in_user['id']) & (BookDatasets.datasets_id==item.id) & (BookDatasets.is_deleted==0)).first()
            if check == None:
                new_db_book = BookDatasets()
                new_db_book.datasets_id = item.id 
                new_db_book.user_id = logged_in_user['id']
                new_db_book.is_deleted = 0
                new_db_book.created_at = datetime.now()
                new_db_book.created_by = logged_in_user['id']

                try:
                    SqlDB.session.add(new_db_book)
                    SqlDB.session.commit()
                except Exception as e:
                    print(e)

        flash('Success book datasets')
        return redirect(url_for('.index'))    

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))
        return render_template('cms/tasks/book.html', data=data, form=form)

    return render_template('cms/tasks/book.html', data=data, form=form)

@tasks.route('/revoke/<int:task_id>')
@login_required
def revoke(task_id):
    logged_in_user = get_user(current_user)

    booking = BookDatasets.query.filter((BookDatasets.id==task_id) & (BookDatasets.user_id==logged_in_user['id'])).first()
    if booking == None:
        return "Access Denied!"
    
    else:
        booking.is_deleted = 1
        booking.updated_at = datetime.now()
        booking.updated_by = logged_in_user['id']

        try:
            SqlDB.session.commit()
        except Exception as e:
            SqlDB.session.rollback()

    return redirect(url_for('.index'))


@tasks.route('/download/<int:task_id>')
@login_required
def download(task_id):
    logged_in_user = get_user(current_user)

    data = {
        'logged_in_user': logged_in_user
    }

    # validate datasets 
    booked_dataset = BookDatasets.query.filter((BookDatasets.id==task_id) & (BookDatasets.user_id==logged_in_user['id']) & (BookDatasets.is_deleted==0)).first()
    if booked_dataset == None:
        return "Access Denied!"
    else:
        # send from directory 
        try:
            hashed_filepath = booked_dataset.dataset.hashed_filepath
            split_path = booked_dataset.dataset.hashed_filepath.split('/')
            if 'app' in split_path[0]:
                hashed_filepath = '/'.join(split_path[1:]) + '/'

            return send_file(''.join([hashed_filepath, booked_dataset.dataset.hashed_filename]), as_attachment=True, attachment_filename=booked_dataset.dataset.hashed_filename)
        except Exception as e:
            return "Something went wrong or dataset not exist anymore"