# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from forms.database import DatabaseForm
from utils.db import db
from utils.organize_data import organize_data
from utils.permissions import Permissions
from models.database import DatabaseModel


databases = Blueprint('databases', __name__)


@databases.route("/database")
def index():
    if Permissions.is_user():
        data = DatabaseModel.query.all()
        show_columns = ['id', 'name', 'host']
        return render_template('/database/index.html', object_list=organize_data(data, show_columns))
    else:
        flash("You do not have permissions")
        return redirect(url_for('index'))


@databases.route("/database/create", methods=['GET', 'POST'])
def create():
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
            flash("Record was inserted successfully")
            return redirect(url_for('databases.index'))

        return render_template('/database/create.html', form=form)
    else:
        flash('You do not have permissions')
        return redirect(url_for('databases.index'))


# recibir parámetro por get
@databases.route("/database/edit/<int:id>", methods=['GET', 'POST'])
def edit(id=0):
    if Permissions.is_admin():
        database = DatabaseModel.query.get(id)
        form = DatabaseForm(obj=database)
        if request.method == 'POST' and form.validate():
            form = DatabaseForm(request.form)
            form.populate_obj(database)
            db.session.add(database)
            db.session.commit()
            flash("Record was updated")
            return redirect(url_for('databases.index'))
        return render_template('/database/create.html', form=form)
    else:
        flash('You do not have permissions')
        return redirect(url_for('databases.index'))


# recibir parámetro por get
@databases.route("/database/delete/<int:id>")
def delete(id=0):
    if Permissions.is_admin():
        database = DatabaseModel.query.get(id)
        db.session.delete(database)
        db.session.commit()
        flash("Record was deleted")
        return redirect(url_for('databases.index'))
    else:
        flash('You do not have permissions')
        return redirect(url_for('databases.index'))
