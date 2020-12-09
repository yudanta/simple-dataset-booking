#!/usr/bin/env python 
import os 
from datetime import datetime
from flask import Blueprint, request, render_template, flash, redirect, url_for 
from flask_login import login_user, logout_user, current_user, login_required 
from app.helpers.getuser import get_user
from app.helpers.generaterandom import generate_random_str
from app.web.datasets.form import AddNewDatasets

from app import SqlDB
from app.models import Datasets

datasets = Blueprint('datasets', __name__, url_prefix='/datasets')

@datasets.route('/')
@login_required
def index():
    logged_in_user = get_user(current_user)

    data = {
        'logged_in_user': logged_in_user
    }

    # load active datasets 
    datasets = Datasets.query.filter((Datasets.status==1) & (Datasets.created_by==logged_in_user['id'])).order_by(Datasets.id.desc()).all()
    data['datasets'] = datasets

    return render_template('cms/datasets/index.html', data=data)

@datasets.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    logged_in_user = get_user(current_user)

    data = {
        'logged_in_user': logged_in_user
    }

    form = AddNewDatasets()
    if form.validate_on_submit():
        hashcode = generate_random_str(16)

        new_datasets = Datasets()
        new_datasets.hashcode = hashcode
        new_datasets.name = form.data['name']
        new_datasets.description = form.data['description']
        new_datasets.status = 1
        new_datasets.created_at = datetime.now()
        new_datasets.created_by = logged_in_user['id']

        # check attachment 
        if form.attachment.data:
            name, ext = os.path.splitext(form.attachment.data.filename)

            upload_file_path = 'app/contentfiles/'
            hashed_filename = ''.join([hashcode, ext])
            local_dirs = ''.join([upload_file_path, datetime.now().strftime('%Y-%m-%d'), '/'])
            local_path = ''.join([local_dirs, hashed_filename])

            # create dirs if not exists 
            if not os.path.exists(os.path.dirname(local_dirs)):
                os.makedirs(os.path.dirname(local_dirs))

            # move to local dirs 
            form.attachment.data.save(local_path)

            # update new_datasets 
            new_datasets.original_file_name = name
            new_datasets.original_file_ext = ext 
            new_datasets.original_file_size = os.stat(local_path).st_size
            new_datasets.hashed_filename = hashed_filename
            new_datasets.hashed_filepath = local_dirs

            # insert 
            SqlDB.session.add(new_datasets)
            SqlDB.session.commit()

            flash('Success add new dataset')
        
        return redirect(url_for('.index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))
        return render_template('cms/datasets/add.html', data=data, form=form)
    
    return render_template('cms/datasets/add.html', data=data, form=form)

@datasets.route('/delete/<int:dataset_id>')
@login_required
def delete(dataset_id):
    logged_in_user = get_user(current_user)

    dataset = Datasets.query.filter((Datasets.id==dataset_id) & (Datasets.status == 1) & (Datasets.created_by==logged_in_user['id'])).first()
    if dataset == None:
        return "Access Denied"
    
    else:
        dataset.status = 0
        dataset.updated_at = datetime.now()
        dataset.updated_by = logged_in_user['id']

        try:
            SqlDB.session.commit()
        except Exception as e:
            SqlDB.session.rollback()
    
    return redirect(url_for('.index'))