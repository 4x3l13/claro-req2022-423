# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 08:30:00 2022

@author: Jhonatan Martínez
"""


from flask import Blueprint, render_template, request
from role import forms, models
from utils import data
from utils.auth import decorator
from utils.db import db
from utils.main_functions import organize_data, show_message

this = "role"
role = Blueprint(this, __name__)
pages = data.pages[this]
routes = data.routes[this]
templates = data.templates[this]


def show_error(message):
    return show_message(id=0,
                        message=message,
                        url=pages["index"] if message.split(sep=".")[1].split(sep=":")[0] != 'index' else 'index')


@role.route(routes["index"])
@decorator(page=pages["index"])
def index():
    try:
        data = organize_data(data_model=models.Role.query.order_by(models.Role.id.desc()).all(),
                             show_columns=['id', 'name'])
        return render_template(templates["index"],
                               object_list=data)
    except Exception as exc:
        return show_error(pages["index"] + ': ' + str(exc))


@role.route(routes["create"], methods=['GET', 'POST'])
@decorator(page=pages["create"], url=pages["index"])
def create():
    try:
        form = forms.CreateForm(request.form)
        if request.method == 'POST' and form.validate():
            data = models.Role(name=form.name.data)
            db.session.add(data)
            db.session.commit()
            return show_message(id=2,
                                url=pages["index"])
        return render_template(templates["create"],
                               form=form)
    except Exception as exc:
        return show_error(pages["create"] + ': ' + str(exc))


# recibir parámetro por get
@role.route(routes["edit"], methods=['GET', 'POST'])
@decorator(page=pages["edit"], url=pages["index"])
def edit(id=0):
    try:
        data = models.Role.query.get(id)
        form = forms.CreateForm(obj=data)
        if request.method == 'POST' and form.validate():
            form = forms.CreateForm(request.form)
            form.populate_obj(data)
            db.session.add(data)
            db.session.commit()
            return show_message(id=3,
                                url=pages["index"])
        return render_template(templates["edit"],
                               form=form)
    except Exception as exc:
        return show_error(pages["edit"] + ': ' + str(exc))


# recibir parámetro por get
@role.route(routes["delete"])
@decorator(page=pages["delete"], url=pages["index"])
def delete(id=0):
    try:
        data = models.Role.query.get(id)
        db.session.delete(data)
        db.session.commit()
        return show_message(id=4,
                            url=pages["index"])
    except Exception as exc:
        return show_error(pages["delete"] + ': ' + str(exc))
