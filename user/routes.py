# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 08:30:00 2022

@author: Jhonatan Martínez
"""


from flask import Blueprint, render_template, request, session
from role.models import Role
from user import forms, models
from utils import data
from utils.auth import decorator
from utils.db import db
from utils.main_functions import  organize_data, show_message

this = "user"
user = Blueprint(this, __name__)
pages = data.pages[this]
routes = data.routes[this]
templates = data.templates[this]


def show_error(message):
    return show_message(id=0,
                        message=message,
                        url=pages["index"] if message.split(sep=".")[1].split(sep=":")[0] != 'index' else 'index')


@user.route(routes["index"])
@decorator(page=pages["index"])
def index():
    try:
        data = organize_data(data_model=models.User.query.order_by(models.User.id.desc()).all(),
                             show_columns=['id', 'full_name', 'email'])
        return render_template(templates["index"],
                               object_list=data)
    except Exception as exc:
        return show_error(pages["index"] + ': ' + str(exc))


@user.route(routes["create"], methods=['GET', 'POST'])
@decorator(page=pages["create"], url=pages["index"])
def create():
    try:
        form = forms.CreateForm(request.form)
        form.role.choices = [(data.id, data.name) for data in Role.query.order_by('name')]
        if request.method == 'POST' and form.validate():
            data = models.User(full_name=form.full_name.data,
                               email=form.email.data,
                               password=form.password.data,
                               is_admin=form.is_admin.data,
                               role_id=form.role.data)
            db.session.add(data)
            db.session.commit()
            return show_message(id=2,
                                url=pages["index"])
        return render_template(templates["create"],
                               form=form)
    except Exception as exc:
        return show_error(pages["create"] + ': ' + str(exc))


# recibir parámetro por get
@user.route(routes["edit"], methods=['GET', 'POST'])
@decorator(page=pages["edit"], url=pages["index"])
def edit(id=0):
    try:
        data = models.User.query.get(id)
        form = forms.CreateForm(obj=data)
        form.role.choices = [(data.id, data.name) for data in Role.query.order_by('name')]
        if request.method == 'POST' and form.validate():
            form = forms.CreateForm(request.form)
            form.password = data.password
            form.populate_obj(data)
            data.password = form.password
            db.session.add(data)
            db.session.commit()
            return show_message(id=3,
                                url=pages["index"])
        return render_template(templates["edit"],
                               form=form)
    except Exception as exc:
        return show_error(pages["edit"] + ': ' + str(exc))


# recibir parámetro por get
@user.route(routes["delete"])
@decorator(page=pages["delete"], url=pages["index"])
def delete(id=0):
    try:
        data = models.User.query.get(id)
        db.session.delete(data)
        db.session.commit()
        return show_message(id=4,
                            url=pages["index"])
    except Exception as exc:
        return show_error(pages["delete"] + ': ' + str(exc))


@user.route(routes["login"], methods=['GET', 'POST'])
def login():
    try:
        form = forms.LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            data = models.User.query.filter_by(email=form.email.data).first()
            if data is not None and data.password == form.password.data:
                session['user'] = data.full_name
                session['user_id'] = data.id
                return show_message(id=6)
            else:
                return show_message(id=7,
                                    url=pages["login"])
        return render_template(templates['login'], form=form)
    except Exception as exc:
        return show_error(pages["login"] + ': ' + str(exc))


@user.route(routes["change_password"], methods=['GET', 'POST'])
def change_password():
    try:
        form = forms.ChangePasswordForm(request.form)
        if request.method == 'POST' and form.validate():
            data = models.User.query.filter_by(id=session['user_id']).first()
            if data is not None and data.password == form.current_password.data:
                data.password = form.new_password.data
                db.session.commit()
                return show_message(id=9,
                                    url=pages["change_password"])
            else:
                show_message(id=10,
                             url=pages["change_password"])
        return render_template(templates['change_password'], form=form)
    except Exception as exc:
        return show_error(pages["index"] + ': ' + str(exc))
