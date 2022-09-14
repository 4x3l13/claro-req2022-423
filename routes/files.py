# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

import inspect
import os
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from forms.file import FileForm, FileUploadForm
from utils.data import messages, months
from utils.db import db
from utils.main_functions import create_directory, organize_data, delete_file
from utils.permissions import Permissions
from models.file import FileModel, UploadedFileModel

files = Blueprint('files', __name__)
this = "routes.files."


def show_message(id=0, message="", url="files.index"):
    flash(message=messages[id][0] if id != 0 else message,
          category=messages[id][1])
    return redirect(url_for(url))


@files.route("/file")
def index():
    try:
        show_columns = ['id', 'name', 'description']
        data = FileModel.query.all()
        return render_template('/file/index.html', object_list=organize_data(data, show_columns))
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


@files.route("/file/create", methods=['GET', 'POST'])
def create():
    try:
        if Permissions.is_user():
            form = FileForm(request.form)
            if request.method == 'POST' and form.validate():
                file = FileModel(name=form.name.data,
                                 description=form.description.data,
                                 columns=form.columns.data)
                db.session.add(file)
                db.session.commit()
                return show_message(id=2)
            return render_template('/file/create.html', form=form)
        else:
            return show_message(id=1)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


# recibir parámetro por get
@files.route("/file/edit/<int:id>", methods=['GET', 'POST'])
def edit(id=0):
    try:
        if Permissions.is_user():
            file = FileModel.query.get(id)
            form = FileForm(obj=file)
            if request.method == 'POST' and form.validate():
                form = FileForm(request.form)
                form.populate_obj(file)
                db.session.add(file)
                db.session.commit()
                return show_message(id=3)
            return render_template('/file/create.html', form=form)
        else:
            return show_message(id=1)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


# recibir parámetro por get
@files.route("/file/delete/<int:id>")
def delete(id=0):
    try:
        if Permissions.is_admin():
            file = FileModel.query.get(id)
            db.session.delete(file)
            db.session.commit()
            return show_message(id=4)
        else:
            return show_message(id=1)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message)


@files.route("/file/historical")
def historical():
    try:
        data = []
        result = db.session.query(UploadedFileModel, FileModel).join(FileModel).all()
        for uploadedfilemodel, filemodel in result:
            data.append({"id": uploadedfilemodel.id, "file": filemodel.name, "year": uploadedfilemodel.year, "month": uploadedfilemodel.month})
        return render_template('/file/historical.html', object_list=data)
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message,
                            url='index')


# recibir parámetro por get
@files.route("/file/upload", methods=['GET', 'POST'])
def upload():
    try:
        if Permissions.is_user():
            form = FileUploadForm(request.form)
            form.file.choices = [(data.id, data.name) for data in FileModel.query.order_by('name')]
            form.year.data = datetime.now().year
            form.month.choices = [(data['id'], data['name']) for data in months]
            if request.method == 'POST':
                directory = create_directory(directory_name="inventory/" + str(form.year.data) + '/' + str(form.month.data))
                file_upload = request.files[form.fileUpload.name]
                file_name = FileModel.query.get(form.file.data).name
                file_upload.save(os.path.join(directory, file_name))
                file = UploadedFileModel(file_id=form.file.data,
                                         year=form.year.data,
                                         month=form.month.data,
                                         directory=directory + "/" + file_name,
                                         user_id=session['user_id'])
                db.session.add(file)
                db.session.commit()
                return  show_message(id=8,
                             url='files.historical')
            return render_template('/file/upload.html', form=form)
        else:
            return show_message(id=1,
                                url='files.historical')
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message,
                            url='files.historical')


# recibir parámetro por get
@files.route("/file/delete_uploaded/<int:id>")
def delete_uploaded(id=0):
    try:
        if Permissions.is_admin():
            uploaded = UploadedFileModel.query.get(id)
            path = "/" + uploaded.directory
            print(path)
            delete_file(path)
            file = UploadedFileModel.query.get(id)
            db.session.delete(file)
            db.session.commit()
            return show_message(id=4,
                                url='files.historical')
        else:
            return show_message(id=1,
                                url='files.historical')
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = this + inspect.stack()[0][3] + ': ' + str(exc)
        return show_message(id=0,
                            message=error_message,
                            url='files.historical')
