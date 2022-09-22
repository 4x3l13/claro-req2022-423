# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""


from wtforms import Form, StringField, TextAreaField, validators


class CreateForm(Form):
    name = StringField('Name',
                       [validators.DataRequired(message="Name is required")])
    description = TextAreaField('Description',
                                [validators.DataRequired(message="Description is required")])
    columns = TextAreaField('Columns (Separated by comma ",")',
                            [validators.DataRequired(message="Columns is required")])
