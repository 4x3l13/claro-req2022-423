# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

import inspect
import cx_Oracle


class Connection:
    """
    Permite la conexión y la obtención de datos desde una Base de Datos ORACLE.

    """

    def __init__(self, host, port, sdi, user, password):
        """
        * **host:** IP o nombre del servidor que aloja la Base de Datos.\n
        * **port:** Puerto del servidor que aloja la Base de Datos.\n
        * **sdi:** Nombre de la Base de Datos a la que se va a conectar.\n
        * **user:** Usuario para conectar a la Base de Datos.\n
        * **password:** Clave para conectar a la Base de Datos.\n
        """

        # Variable que almacena el nombre de la clase
        self.__this = self.__class__.__name__ + '.'
        # Variable de conexión
        self.__connection = None
        # Diccionario que almacena los datos para la conexión
        self.__connection_data = {"HOST": host, "PORT": port, "SDI": sdi, "USER": user, "PASSWORD": password}
        try:
            # Carga las librerías cliente de Oracle
            cx_Oracle.init_oracle_client(lib_dir=r"F:\oracle\instantclient_11_2")
        except Exception as exc:
            print("ERROR: " + exc)

    def _close_connection(self):
        """
        Cierra la conexión a la Base de Datos.
        """

        try:
            self.__connection.close()
        except Exception as exc:
            # Variable error_message almacena la clase, el método y el error
            error_message = self.__this + inspect.stack()[0][3] + ': ' + str(exc)
            print("ERROR: " + error_message)

    def _open_connection(self):
        """
        Obtiene la conexión a la Base de Datos.
        """

        try:
            # Variable dsn almacena al configuración del dsn
            dsn = self.__connection_data["HOST"] + ":" + self.__connection_data["PORT"] + "/" + self.__connection_data["SDI"]
            # Crear la conexión
            self.__connection = cx_Oracle.connect(user=self.__connection_data["USER"],
                                                  password=self.__connection_data["PASSWORD"],
                                                  dsn=dsn,
                                                  encoding="UTF-8")
        except Exception as exc:
            # Variable error_message almacena la clase, el método y el error
            error_message = self.__this + inspect.stack()[0][3] + ': ' + str(exc)
            print("ERROR: " + error_message)

    def read_data(self, query, datatype="dict"):
        """
        Obtiene los resulta de una consulta a base de datos y lo devuelve en diccionario o lista.

        Params:
            * **query (Str):** Consulta a realizar \n
            * **datatype (Str):** Tipo de dato a devolver, admite(dict, list). \n

        Returns:

        """

        try:
            self._open_connection()
            # Crear el cursor.
            cursor = self.__connection.cursor()
            # Configurar los tamaños que recibe el cursor
            cursor.prefetchrows = 100000
            cursor.arraysize = 100000
            # Ejecutar la consulta
            cursor.execute(query)
            # Variable data almacena los datos obtenidos de la consulta
            data = cursor.fetchall()
            # GVariable columns almacena el nombre de las columnas de la consulta
            columns = [column[0].upper() for column in cursor.description]
            # Validar que tipo de dato vamos a devolver
            if datatype == 'dict':
                dictionary = []
                for item in data:
                    dictionary.append(dict(zip(columns, item)))
                return dictionary
            elif datatype == 'list':
                return [columns, data]
            cursor.close()
        except (ConnectionError, Exception) as exc:
            # Variable error_message almacena la clase, el método y el error
            error_message = self.__this + inspect.stack()[0][3] + ': ' + str(exc)
            print("ERROR: " + error_message)
        finally:
            self._close_connection()
