# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 08:30:00 2022

@author: Jhonatan Martínez
"""

import datetime
from utils.db import db


class FileModel(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(1000))
    columns = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)


class UploadedFileModel(db.Model):
    __tablename__ = 'uploadedfiles'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    year = db.Column(db.String(4))
    month = db.Column(db.String(2))
    directory = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
