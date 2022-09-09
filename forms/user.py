# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

from wtforms import BooleanField, EmailField, Form, PasswordField, StringField, validators


class UserForm(Form):
    full_name = StringField('Full Name',
                            [validators.DataRequired(message="Full Name is required")])
    email = EmailField('Email',
                       [validators.DataRequired(message="Email is required")])
    password = PasswordField('Password',
                             [validators.DataRequired(message="Password is required")])
    is_admin = BooleanField('Is Admin?')


class LoginForm(Form):
    email = EmailField('Email',
                       [validators.DataRequired(message="Email is required")])
    password = PasswordField('Password',
                             [validators.DataRequired(message="Password is required")])
