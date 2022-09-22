# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import Form, IntegerField, SelectField, validators


class CreateForm(Form):
    file = SelectField('File',
                       [validators.DataRequired(message="File is required")])
    year = IntegerField('Year',
                        [validators.DataRequired(message="Year is required")])
    month = SelectField('Month',
                        [validators.DataRequired(message="Month is required")])
    fileUpload = FileField('File to Upload',
                           validators=[FileRequired(message="File to Upload is required"),
                                       FileAllowed(['xls', 'xlsx'], 'Log and Excel Document only!')])
