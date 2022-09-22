from functools import wraps

from flask import session
from user.models import User
from permission.models import Permission
from page.models import Page
from utils.main_functions import show_message


def has_permission(page):
    can_enter = False
    try:
        user = User.query.get(session['user_id'])
        if user.is_admin:
            can_enter = True
        else:
            page_id = Page.query.filter(Page.route == page).first().id
            permissions = Permission.query.filter_by(role_id=user.role_id, page_id=page_id).first()
            if permissions is not None:
                can_enter = True
    except Exception as exc:
        # Variable error_message almacena la clase, el método y el error
        error_message = 'permission.queries.has_permission: ' + str(exc)
        print(error_message)
    finally:
        return can_enter


def decorator(page, url='index'):
    def _permissions(function):
        @wraps(function)
        def new_function(*args, **kwargs):
            if not has_permission(page=page):
                return show_message(id=1,
                                    url=url)
            return function(*args, **kwargs)
        return new_function

    return _permissions