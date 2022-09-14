# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

import inspect
from flask import session
from models.user import UserModel


class Permissions:
    """
    Válida el tipo de usuario para otorgar permiso de ingreso a la página
    """

    @staticmethod
    def is_user():
        """
        Válida si es un usuario (Si ha iniciado sesión)

        Returns:
            value(Boolean)
        """
        value = False
        try:
            # Válida si hay una sesión de usuario
            if 'user' in session:
                value = True
        except Exception as exc:
            # Variable error_message almacena la clase, el método y el error
            error_message = 'Permissions.' + inspect.stack()[0][3] + ': ' + str(exc)
            print(error_message)
        finally:
            return value

    @staticmethod
    def is_admin():
        """
        Válida si es un usuario (Si ha iniciado sesión) y si este es administrador

        Returns:
            value(Boolean)
        """
        value = False
        try:
            if Permissions.is_user():
                user = UserModel.query.get(session['user_id'])
                value = user.is_admin
        except Exception as exc:
            # Variable error_message almacena la clase, el método y el error
            error_message = 'Permissions.' + inspect.stack()[0][3] + ': ' + str(exc)
            print(error_message)
        finally:
            return value
