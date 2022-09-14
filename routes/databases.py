# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

import inspect
from flask import Blueprint, flash, redirect, render_template, request, url_for
from forms.database import DatabaseForm
from utils.data import messages
from utils.db import db
from utils.main_functions import organize_data
from utils.permissions import Permissions
from models.database import DatabaseModel


databases = Blueprint('databases', __name__)
this = "routes.databases."


def show_message(id=0, message="", url="databases.index"):
    flash(message=messages[id][0] if id != 0 else message,
          category=messages[id][1])
    return redirect(url_for(url))


@databases.route("/database")
def index():
    try:
        if Permissions.is_admin():
            show_columns = ['id', 'name', 'host']
            data = DatabaseModel.query.all()
            return render_template('/database/index.html',
                                   object_list=organize_data(data, show_columns))
        else:
            return show_message(id=1,
                                url="index")
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


@databases.route("/database/create", methods=['GET', 'POST'])
def create():
    try:
        if Permissions.is_admin():
            form = DatabaseForm(request.form)
            if request.method == 'POST' and form.validate():
                database = DatabaseModel(name=form.name.data,
                                         host=form.host.data,
                                         port=form.port.data,
                                         sdi=form.sdi.data,
                                         user=form.user.data,
                                         password=form.password.data)
                db.session.add(database)
                db.session.commit()
                return show_message(id=2)
            return render_template('/database/create.html', form=form)
        else:
            return show_message(id=1)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


# recibir parámetro por get
@databases.route("/database/edit/<int:id>", methods=['GET', 'POST'])
def edit(id=0):
    try:
        if Permissions.is_admin():
            database = DatabaseModel.query.get(id)
            form = DatabaseForm(obj=database)
            if request.method == 'POST' and form.validate():
                form = DatabaseForm(request.form)
                form.populate_obj(database)
                db.session.add(database)
                db.session.commit()
                return show_message(id=3)
            return render_template('/database/create.html', form=form)
        else:
            return show_message(id=1)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


# recibir parámetro por get
@databases.route("/database/delete/<int:id>")
def delete(id=0):
    try:
        if Permissions.is_admin():
            database = DatabaseModel.query.get(id)
            db.session.delete(database)
            db.session.commit()
            return show_message(id=4)
        else:
            return show_message(id=1)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)
