# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""


from wtforms import Form, IntegerField, StringField, validators


class DatabaseForm(Form):
    name = StringField('Name',
                       [validators.DataRequired(message="Name is required")])
    host = StringField('Host',
                       [validators.DataRequired(message="Host is required")])
    port = IntegerField('Port',
                        [validators.DataRequired(message="Port is required")])
    sdi = StringField('SDI',
                      [validators.DataRequired(message="SDI is required")])
    user = StringField('User',
                       [validators.DataRequired(message="User is required")])
    password = StringField('Password',
                           [validators.DataRequired(message="Password is required")])
