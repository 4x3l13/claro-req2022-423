# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

import inspect
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from forms.user import UserForm, LoginForm
from utils.data import messages
from utils.db import db
from utils.main_functions import organize_data
from utils.permissions import Permissions
from models.user import UserModel


users = Blueprint('users', __name__)
this = "routes.users."


def show_message(id=0, message="", url="users.index"):
    flash(message=messages[id][0] if id != 0 else message,
          category=messages[id][1])
    return redirect(url_for(url))


@users.route("/user")
def index():
    try:
        if Permissions.is_user():
            show_columns = ['id', 'full_name', 'email']
            data = UserModel.query.all()
            return render_template('/user/index.html', object_list=organize_data(data, show_columns))
        else:
            return show_message(id=1,
                                url="index")
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


@users.route("/user/create", methods=['GET', 'POST'])
def create():
    try:
        if Permissions.is_admin():
            form = UserForm(request.form)
            if request.method == 'POST' and form.validate():
                user = UserModel(full_name=form.full_name.data,
                                 email=form.email.data,
                                 password=form.password.data,
                                 is_admin=form.is_admin.data)
                db.session.add(user)
                db.session.commit()
                return show_message(id=2)
            return render_template('/user/create.html', form=form)
        else:
            return show_message(id=1)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


# recibir parámetro por get
@users.route("/user/edit/<int:id>", methods=['GET', 'POST'])
def edit(id=0):
    try:
        if Permissions.is_admin():
            user = UserModel.query.get(id)
            form = UserForm(obj=user)
            if request.method == 'POST' and form.validate():
                form = UserForm(request.form)
                form.populate_obj(user)
                db.session.add(user)
                db.session.commit()
                return show_message(id=3)
            return render_template('/user/create.html', form=form)
        else:
            return show_message(id=1)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


# recibir parámetro por get
@users.route("/user/delete/<int:id>")
def delete(id=0):
    try:
        if Permissions.is_admin():
            user = UserModel.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return show_message(id=4)
        else:
            return show_message(id=1)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


@users.route("/user/login", methods=['GET', 'POST'])
def login():
    try:
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            user = UserModel.query.filter_by(email= form.email.data).first()
            if user is not None and user.password == form.password.data:
                message = "Welcome!"
                session['user'] = user.full_name
                session['user_id'] = user.id
                return show_message(id=6,
                                    url='index')
            else:
                show_message(id=7,
                             url='users.login')
        return render_template('/user/login.html', form=form)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message,
                            url='users.login')
