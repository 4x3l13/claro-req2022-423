# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

import datetime
from utils.db import db


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
