# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""


def organize_data(data_model, show_columns):
    """
    Organiza la data de modelos en listas con diccionarios para mostrar en los index

    Params:
            * **dataModel (Model):** Datos del modelo del ORM. \n
            * **show_columns (List):** Lista con los campos que se van a mostrar en el index. \n
            * **file_name (Str):** Nombre con el que se va a descargar el archivo. \n

        Returns:
            object_list
    """

    object_list = []
    # Recorrer cada fila devuelta por el modelo del ORM
    for row in data_model:
        # Variable dictionary almacena en formato diccionario cada fila del modelo del ORM
        dictionary = dict((column, getattr(row, column)) for column in row.__table__.columns.keys())
        delete_columns = []
        # Recorre las keys del diccionario
        for key in dictionary.keys():
            # Válida si la key está en las columnas que vamos a mostrar
            if key not in show_columns:
                # Almacena las keys que no se van a mostrar
                delete_columns.append(key)
        # For para eliminar las keys que no se van a mostrar
        for column in delete_columns:
            dictionary.pop(column)
        object_list.append(dictionary)
    return object_list
