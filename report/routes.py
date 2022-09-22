# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 08:30:00 2022

@author: Jhonatan Martínez
"""


from flask import Blueprint, render_template, request
from report import forms, models
from database.models import Database
from utils import data
from utils.auth import decorator
from utils.db import db
from utils.connection import Connection
from utils.main_functions import download_excel, organize_data, show_message

this = "report"
report = Blueprint(this, __name__)
pages = data.pages[this]
routes = data.routes[this]
templates = data.templates[this]


def show_error(message):
    return show_message(id=0,
                        message=message,
                        url=pages["index"] if message.split(sep=".")[1].split(sep=":")[0] != 'index' else 'index')


@report.route(routes["index"])
@decorator(page=pages["index"])
def index():
    try:
        data = organize_data(data_model=models.Report.query.order_by(models.Report.id.desc()).all(),
                             show_columns=['id', 'name', 'description'])
        return render_template(templates["index"],
                               object_list=data)
    except Exception as exc:
        return show_error(pages["index"] + ': ' + str(exc))


@report.route(routes["create"], methods=['GET', 'POST'])
@decorator(page=pages["create"], url=pages["index"])
def create():
    try:
        form = forms.CreateForm(request.form)
        form.database_id.choices = [(data.id, data.name) for data in Database.query.all()]
        if request.method == 'POST' and form.validate():
            data = models.Report(name=form.name.data,
                                 description=form.description.data,
                                 queries=form.queries.data,
                                 params=form.params.data,
                                 database_id=form.database_id.data)
            db.session.add(data)
            db.session.commit()
            return show_message(id=2,
                                url=pages["index"])
        return render_template(templates["create"],
                               form=form)
    except Exception as exc:
        return show_error(pages["create"] + ': ' + str(exc))


# recibir parámetro por get
@report.route(routes["edit"], methods=['GET', 'POST'])
@decorator(page=pages["edit"], url=pages["index"])
def edit(id=0):
    try:
        data = models.Report.query.get(id)
        form = forms.CreateForm(obj=data)
        form.database_id.choices = [(data.id, data.name) for data in Database.query.all()]
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
@report.route(routes["delete"])
@decorator(page=pages["delete"], url=pages["index"])
def delete(id=0):
    try:
        data = models.Report.query.get(id)
        db.session.delete(data)
        db.session.commit()
        return show_message(id=4,
                            url=pages["index"])
    except Exception as exc:
        return show_error(pages["delete"] + ': ' + str(exc))


@report.route(routes["download"])
@decorator(page=pages["download"], url=pages["index"])
def download(id=0):
    try:
        result = models.Report.query.get(id)
        database = Database.query.get(result.database_id)
        cnx = Connection(database.host, database.port, database.sdi, database.user, database.password)
        data = cnx.read_data(query=result.queries, datatype="list")
        return download_excel(columns=data[0],
                              rows=data[1],
                              file_name=result.name + ".xlsx")
    except Exception as exc:
        return show_error(pages["download"] + ': ' + str(exc))
