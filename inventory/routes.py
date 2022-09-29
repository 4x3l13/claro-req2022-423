# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 08:30:00 2022

@author: Jhonatan Martínez
"""


from datetime import datetime
from flask import Blueprint, render_template, request, session, send_file
from inventory import forms, models
from utils import data
from utils.auth import decorator
from utils.data import months
from utils.db import db
from utils.inventory import Inventory
from utils.main_functions import delete_file, organize_data, show_message

this = "inventory"
inventory = Blueprint(this, __name__)
pages = data.pages[this]
routes = data.routes[this]
templates = data.templates[this]


def show_error(message):
    print(message.split(sep=".")[1].split(sep=":")[0])
    print(pages["index"])
    return show_message(id=0,
                        message=message,
                        url=pages["index"] if message.split(sep=".")[1].split(sep=":")[0] != 'index' else 'index')


@inventory.route(routes["index"])
@decorator(page=pages["index"])
def index():
    try:
        data = organize_data(data_model=models.Inventory.query.order_by(models.Inventory.id.desc()).all(),
                             show_columns=['id', 'year', 'month', 'directory'])
        for row in data:
            file = row["directory"].split(sep="/")[-1]
            row["file"] = file
        return render_template(templates["index"],
                               object_list=data)
    except Exception as exc:
        return show_error(pages["index"] + ': ' + str(exc))


@inventory.route(routes["create"], methods=['GET', 'POST'])
@decorator(page=pages["create"], url=pages["index"])
def create():
    try:
        form = forms.CreateForm(request.form)
        form.year.data = datetime.now().year
        form.month.choices = [(data['id'], data['name']) for data in months]
        if request.method == 'POST' and form.validate():
            data_exist = models.Inventory.query.filter_by(year=form.year.data, month=form.month.data).first()
            if data_exist is None:
                obj_inventory = Inventory(form.year.data, form.month.data)
                invetory_file, missing_file = obj_inventory.run()
                data = models.Inventory(year=form.year.data,
                                        month=form.month.data,
                                        directory=invetory_file,
                                        user_id=session['user_id'])
                db.session.add(data)
                db.session.commit()
                data = models.Inventory(year=form.year.data,
                                        month=form.month.data,
                                        directory=missing_file,
                                        user_id=session['user_id'])
                db.session.add(data)
                db.session.commit()
                return show_message(id=2,
                                    url=pages["index"])
            return show_message(id=11,
                                url=pages["index"])
        return render_template(templates["create"],
                               form=form)
    except Exception as exc:
        return show_error(pages["create"] + ': ' + str(exc))


# recibir parámetro por get
@inventory.route(routes["delete"])
@decorator(page=pages["delete"], url=pages["index"])
def delete(id=0):
    try:
        data = models.Inventory.query.get(id)
        path = data.directory
        delete_file(path, fullpath=True)
        db.session.delete(data)
        db.session.commit()
        return show_message(id=4,
                            url=pages["index"])
    except Exception as exc:
        return show_error(pages["delete"] + ': ' + str(exc))


@inventory.route(routes["download"])
@decorator(page=pages["download"], url=pages["index"])
def download(id=0):
    try:
        data = models.Inventory.query.get(id)
        return send_file(data.directory, as_attachment=True)
    except Exception as exc:
        return show_error(pages["delete"] + ': ' + str(exc))