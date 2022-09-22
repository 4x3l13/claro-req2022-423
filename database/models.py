# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

import datetime
from utils.db import db


class Database(db.Model):
    __tablename__ = 'databases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    host = db.Column(db.String(100))
    port = db.Column(db.String(10))
    sdi = db.Column(db.String(100))
    user = db.Column(db.String(100))
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
