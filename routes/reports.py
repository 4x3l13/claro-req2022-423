# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""
import inspect
from flask import Blueprint, flash, redirect, render_template, request, url_for
from forms.report import ReportForm
from utils.connection import Connection
from utils.data import messages
from utils.db import db
from utils.main_functions import download_excel, organize_data
from utils.permissions import Permissions
from models.report import ReportModel
from models.database import DatabaseModel


reports = Blueprint('reports', __name__)
this = "routes.reports."


def show_message(id=0, message="", url="reports.index"):
    flash(message=messages[id][0] if id != 0 else message,
          category=messages[id][1])
    return redirect(url_for(url))


@reports.route("/report")
def index():
    try:
        show_columns = ['id', 'name', 'description']
        data = ReportModel.query.all()
        return render_template('/report/index.html',
                               object_list=organize_data(data, show_columns))
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


@reports.route("/report/create", methods=['GET', 'POST'])
def create():
    try:
        if Permissions.is_user():
            form = ReportForm(request.form)
            form.database_id.choices = [(data.id, data.name) for data in DatabaseModel.query.order_by('name')]
            if request.method == 'POST' and form.validate():
                report = ReportModel(name=form.name.data,
                                     description=form.description.data,
                                     queries=form.queries.data,
                                     params=form.params.data,
                                     database_id=form.database_id.data)
                db.session.add(report)
                db.session.commit()
                return show_message(id=2)
            return render_template('/report/create.html', form=form)
        else:
            return show_message(id=1)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


# recibir parámetro por get
@reports.route("/report/edit/<int:id>", methods=['GET', 'POST'])
def edit(id=0):
    try:
        if Permissions.is_user():
            report = ReportModel.query.get(id)
            form = ReportForm(obj=report)
            form.database_id.choices = [(data.id, data.name) for data in DatabaseModel.query.order_by('name')]
            if request.method == 'POST' and form.validate():
                form = ReportForm(request.form)
                form.database_id.choices = [(data.id, data.name) for data in DatabaseModel.query.order_by('name')]
                form.populate_obj(report)
                db.session.add(report)
                db.session.commit()
                return show_message(id=3)
            return render_template('/report/create.html', form=form)
        else:
            return show_message(id=1)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


# recibir parámetro por get
@reports.route("/report/delete/<int:id>")
def delete(id=0):
    try:
        if Permissions.is_admin():
            report = ReportModel.query.get(id)
            db.session.delete(report)
            db.session.commit()
            return show_message(id=4)
        else:
            return show_message(id=1)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


# recibir parámetro por get
@reports.route("/report/download/<int:id>")
def download(id=0):
    try:
        report = ReportModel.query.get(id)
        database = DatabaseModel.query.get(report.database_id)
        cnx = Connection(database.host, database.port, database.sdi, database.user, database.password)
        data = cnx.read_data(query=report.queries, datatype="list")
        return download_excel(columns=data[0],
                              rows=data[1],
                              file_name=report.name + ".xlsx")
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)
