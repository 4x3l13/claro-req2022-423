# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from forms.user import UserForm, LoginForm
from utils.db import db
from utils.organize_data import organize_data
from utils.permissions import Permissions
from models.user import UserModel


users = Blueprint('users', __name__)


@users.route("/user")
def index():
    if Permissions.is_user():
        data = UserModel.query.all()
        show_columns = ['id', 'full_name', 'email']
        return render_template('/user/index.html', object_list=organize_data(data, show_columns))
    else:
        flash('You do not have permissions')
        return redirect(url_for('index'))


@users.route("/user/create", methods=['GET', 'POST'])
def create():
    if Permissions.is_admin():
        form = UserForm(request.form)
        if request.method == 'POST' and form.validate():
            user = UserModel(full_name=form.full_name.data,
                             email=form.email.data,
                             password=form.password.data,
                             is_admin=form.is_admin.data)
            db.session.add(user)
            db.session.commit()
            flash("Record was inserted successfully")
            return redirect(url_for('users.index'))

        return render_template('/user/create.html', form=form)
    else:
        flash('You do not have permissions')
        return redirect(url_for('users.index'))


# recibir parámetro por get
@users.route("/user/edit/<int:id>", methods=['GET', 'POST'])
def edit(id=0):
    if Permissions.is_admin():
        user = UserModel.query.get(id)
        form = UserForm(obj=user)
        if request.method == 'POST' and form.validate():
            form = UserForm(request.form)
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            flash("Record was updated")
            return redirect(url_for('users.index'))
        return render_template('/user/create.html', form=form)
    else:
        flash('You do not have permissions')
        return redirect(url_for('users.index'))


# recibir parámetro por get
@users.route("/user/delete/<int:id>")
def delete(id=0):
    if Permissions.is_admin():
        user = UserModel.query.get(id)
        db.session.delete(user)
        db.session.commit()
        flash("Record was deleted")
        return redirect(url_for('users.index'))
    else:
        flash('You do not have permissions')
        return redirect(url_for('users.index'))


@users.route("/user/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = UserModel.query.filter_by(email= form.email.data).first()
        if user is not None and user.password == form.password.data:
            message = "Welcome!"
            session['user'] = user.full_name
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            message = "User or password is not valid"
        flash(message)

    return render_template('/user/login.html', form=form)
