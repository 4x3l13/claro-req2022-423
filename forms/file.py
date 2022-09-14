# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 08:30:00 2022

@author: Jhonatan Martínez
"""
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import Form, IntegerField, SelectField, StringField, TextAreaField, validators


class FileForm(Form):
    name = StringField('Name',
                       [validators.DataRequired(message="Name is required")])
    description = TextAreaField('Description',
                                [validators.DataRequired(message="Description is required")])
    columns = TextAreaField('Columns (Separated by comma ",")',
                            [validators.DataRequired(message="Columns is required")])


class FileUploadForm(Form):
    file = SelectField('File',
                       [validators.DataRequired(message="File is required")])
    year = IntegerField('Year',
                        [validators.DataRequired(message="Year is required")])
    month = SelectField('Month',
                        [validators.DataRequired(message="Month is required")])
    fileUpload = FileField('File to Upload',
                           validators=[FileRequired(message="File to Upload is required"),
                                       FileAllowed(['xls', 'xlsx'], 'Log and Excel Document only!')])
