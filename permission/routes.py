# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 08:30:00 2022

@author: Jhonatan Martínez
"""


from flask import Blueprint, render_template, request
from page.models import Page
from permission import models
from role.models import Role
from utils import data
from utils.auth import decorator
from utils.db import db
from utils.main_functions import organize_data, show_message

this = "permission"
permission = Blueprint(this, __name__)
pages = data.pages[this]
routes = data.routes[this]
templates = data.templates[this]


def show_error(message):
    return show_message(id=0,
                        message=message,
                        url=pages["index"])


# recibir parámetro por get
@permission.route(routes["edit"], methods=['GET', 'POST'])
@decorator(page=pages["edit"], url=pages["index"])
def edit(id=0):
    try:
        show_columns_pages = ['id', 'name']
        if request.method == 'POST':
            page = request.values['submit_param']
            action, identification = page.split(sep=".")
            if action == 'add':
                create(id, identification)
            elif action == 'del':
                delete(identification)
        result = db.session.query(models.Permission, Role, Page).join(Role, Page).filter(Role.id == id).all()
        permissions_, pages_in = [], []
        for permission_, role, page in result:
            permissions_.append({"id": permission_.id, "page": page.name})
            pages_in.append(page.id)
        pages_ = Page.query.filter(Page.id.not_in(pages_in)).all()
        return render_template(templates["edit"], object_list=[permissions_, organize_data(pages_, show_columns_pages)])
    except Exception as exc:
        return show_error(pages["index"] + ': ' + str(exc))


def create(role, page):
    data = models.Permission(role_id=role,
                             page_id=page)
    db.session.add(data)
    db.session.commit()


def delete(id):
    data = models.Permission.query.get(id)
    db.session.delete(data)
    db.session.commit()