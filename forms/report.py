# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

from wtforms import Form, SelectField, StringField, TextAreaField, validators


class ReportForm(Form):
    name = StringField('Name',
                       [validators.DataRequired(message="Name is required")]
                       )
    description = TextAreaField('Description',
                                [validators.DataRequired(message="Description is required")]
                                )
    queries = TextAreaField('Queries',
                          [validators.DataRequired(message="Queries is required")]
                          )
    params = TextAreaField('Parameters')
    database_id = SelectField('Database', coerce=int)
