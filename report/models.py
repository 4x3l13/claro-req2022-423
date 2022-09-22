# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

import datetime
from utils.db import db


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(1000))
    queries = db.Column(db.String(5000))
    params = db.Column(db.String(5000))
    database_id = db.Column(db.Integer, db.ForeignKey('databases.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
