# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import CSRFProtect
import logging
from config import DevelopmentConfig, QualityConfig
from utils.db import db
from routes.databases import databases
from routes.reports import reports
from routes.users import users


# Inicializar el objeto
app = Flask(__name__, template_folder='templates')
app.config.from_object(QualityConfig)
csrf = CSRFProtect(app)

app.register_blueprint(reports)
app.register_blueprint(databases)
app.register_blueprint(users)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


# Decorador
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    # Retorno de la función
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Ejecuta el servidor default port 5000
    # El debug en true permite ver cambios mientras se está editando
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        print(db.create_all())
    logging.basicConfig(filename='Log/myapp.log', level=logging.DEBUG)
    app.run(host="0.0.0.0", port=8000)
