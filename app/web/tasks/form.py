#!/usr/bin/env python 
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, BooleanField, widgets, RadioField, DecimalField
from wtforms.validators import Required, Email, Length, EqualTo
from wtforms.validators import Required, Length
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField

from flask_login import login_user, logout_user, current_user, login_required 
from app.helpers.getuser import get_user

from app import app, SqlDB
from app.models import Datasets, Users, BookDatasets

def get_active_datasets():
    # get list book datasets first from existing users 
    booked_ids = Datasets.query.join(BookDatasets, BookDatasets.datasets_id==Datasets.id).filter((BookDatasets.user_id==current_user.id) & (BookDatasets.is_deleted==0)).with_entities(Datasets.id)
    print('booked ids', booked_ids)
    return Datasets.query.filter(~Datasets.id.in_(booked_ids)).all()

    # datasets = Datasets.query.filter((Datasets.status==1) & (Datasets.id.))
    # return Datasets.query.filter(Datasets.status==1).all()

class AddNewBookingTask(Form):
    datasets = QuerySelectMultipleField('datasets', 
        query_factory=get_active_datasets, 
        widget=widgets.ListWidget(prefix_label=False), 
        allow_blank=False, 
        option_widget=widgets.CheckboxInput(),
        get_pk=lambda d: d.id,
        get_label=lambda d: d.name
    )
    submit = SubmitField('submit')

# EditBookingTask = model_form(

# )
