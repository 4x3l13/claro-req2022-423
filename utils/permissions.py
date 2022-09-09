# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

from flask import session
from models.user import UserModel


class Permissions:
    """
    Valida el tipo de usuario para otorgar permiso de ingreso a la página
    """

    @staticmethod
    def is_user():
        """
        Válida si es un usuario (Si ha iniciado sesión)

        Returns:
            value(Boolean)
        """

        value = False
        # Válida si hay una sesión de usuario
        if 'user' in session:
            value = True
        return value

    @staticmethod
    def is_admin():
        """
        Válida si es un usuario (Si ha iniciado sesión) y si este es administrador

        Returns:
            value(Boolean)
        """

        value = False
        if Permissions.is_user():
            user = UserModel.query.get(session['user_id'])
            value = user.is_admin
        return value
