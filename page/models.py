# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

import datetime
from utils.db import db


class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    permissions = db.relationship('Permission', cascade='all, delete', backref='page')
