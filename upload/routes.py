# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 08:30:00 2022

@author: Jhonatan Martínez
"""


from datetime import datetime
import os
from flask import Blueprint, render_template, request, session
from file.models import File
from upload import forms, models
from utils import data
from utils.auth import decorator
from utils.data import months
from utils.db import db
from utils.main_functions import create_directory, delete_file, show_message

this = "upload"
upload = Blueprint(this, __name__)
pages = data.pages[this]
routes = data.routes[this]
templates = data.templates[this]


def show_error(message):
    return show_message(id=0,
                        message=message,
                        url=pages["index"] if message.split(sep=".")[1].split(sep=":")[0] != 'index' else 'index')


@upload.route(routes["index"])
@decorator(page=pages["index"])
def index():
    try:
        data = []
        result = db.session.query(models.Upload, File).join(File).order_by(models.Upload.id.desc()).all()
        for upload_, file in result:
            data.append({"id": upload_.id, "file": file.name, "year": upload_.year, "month": upload_.month})
        return render_template(templates["index"],
                               object_list=data)
    except Exception as exc:
        return show_error(pages["index"] + ': ' + str(exc))


@upload.route(routes["create"], methods=['GET', 'POST'])
@decorator(page=pages["create"], url=pages["index"])
def create():
    try:
        form = forms.CreateForm(request.form)
        form.file.choices = [(data.id, data.name) for data in File.query.all()]
        form.year.data = datetime.now().year
        form.month.choices = [(data['id'], data['name']) for data in months]
        if request.method == 'POST':
            path = "files/" + str(form.year.data) + '/' + str(form.month.data)
            directory = create_directory(directory_name=path)
            file_upload = request.files[form.fileUpload.name]
            file_name = File.query.get(form.file.data).name
            file_upload.save(os.path.join(directory, file_name))
            data = models.Upload(file_id=form.file.data,
                                 year=form.year.data,
                                 month=form.month.data,
                                 directory=directory + "/" + file_name,
                                 user_id=session['user_id'])
            db.session.add(data)
            db.session.commit()
            return show_message(id=2,
                                url=pages["index"])
        return render_template(templates["create"],
                               form=form)
    except Exception as exc:
        return show_error(pages["create"] + ': ' + str(exc))


# recibir parámetro por get
@upload.route(routes["delete"])
@decorator(page=pages["delete"], url=pages["index"])
def delete(id=0):
    try:
        data = models.Upload.query.get(id)
        path = "/" + data.directory
        delete_file(path)
        db.session.delete(data)
        db.session.commit()
        return show_message(id=4,
                            url=pages["index"])
    except Exception as exc:
        return show_error(pages["delete"] + ': ' + str(exc))
