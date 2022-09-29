# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""


from wtforms import Form, IntegerField, SelectField, validators


class CreateForm(Form):
    year = IntegerField('Year',
                        [validators.DataRequired(message="Year is required")])
    month = SelectField('Month',
                        [validators.DataRequired(message="Month is required")])
