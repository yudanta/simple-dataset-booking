#!/usr/bin/env python 
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, BooleanField, widgets, RadioField, DecimalField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Required, Length
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField

from app import app, SqlDB

class AddNewDatasets(Form):
    name = TextField('name', [Required(), Length(max=150)])
    description = TextAreaField('description', [Length(max=255)])
    attachment = FileField('attachment', validators=[FileAllowed(['zip'], 'Only Zip Attachment Allowed!'), Required()])
    submit = SubmitField('submit')