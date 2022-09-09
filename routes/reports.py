# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from forms.report import ReportForm
from utils.connection import Connection
from utils.db import db
from utils.excel import Excel
from utils.organize_data import organize_data
from utils.permissions import Permissions
from models.report import ReportModel
from models.database import DatabaseModel


reports = Blueprint('reports', __name__)


@reports.route("/report")
def index():
    data = ReportModel.query.all()
    show_columns = ['id', 'name', 'description']
    return render_template('/report/index.html', object_list=organize_data(data, show_columns))


@reports.route("/report/create", methods=['GET', 'POST'])
def create():
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
            flash("Record was inserted successfully")
            return redirect(url_for('reports.index'))
        return render_template('/report/create.html', form=form)
    else:
        flash('You do not have permissions')
        return redirect(url_for('reports.index'))


# recibir parámetro por get
@reports.route("/report/edit/<int:id>", methods=['GET', 'POST'])
def edit(id=0):
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
            flash("Record was updated")
            return redirect(url_for('reports.index'))
        return render_template('/report/create.html', form=form)
    else:
        flash('You do not have permissions')
        return redirect(url_for('reports.index'))


# recibir parámetro por get
@reports.route("/report/delete/<int:id>")
def delete(id=0):
    if Permissions.is_admin():
        report = ReportModel.query.get(id)
        db.session.delete(report)
        db.session.commit()
        flash("Record was deleted")
        return redirect(url_for('reports.index'))
    else:
        flash('You do not have permissions')
        return redirect(url_for('reports.index'))


# recibir parámetro por get
@reports.route("/report/download/<int:id>")
def download(id=0):
    report = ReportModel.query.get(id)
    database = DatabaseModel.query.get(report.database_id)
    cnx = Connection(database.host, database.port, database.sdi, database.user, database.password)
    data = cnx.read_data(query=report.queries, datatype="list")
    return Excel.download(columns=data[0],
                          rows=data[1],
                          file_name=report.name + ".xlsx")
