# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""


from wtforms import Form, StringField, validators


class CreateForm(Form):
    name = StringField('Name',
                       [validators.DataRequired(message="Name is required")])
