# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:30:00 2022

@author: Jhonatan Martínez
"""

from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from utils.db import db
from utils.email import email
from database.routes import database
from file.routes import file
from page.routes import page
from permission.routes import permission
from report.routes import report
from role.routes import role
from upload.routes import upload
from user.routes import user


# Inicializar el objeto
# app = Flask(__name__, template_folder='templates')
app = Flask(__name__)
# app.config.from_object(QualityConfig)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

app.register_blueprint(database)
app.register_blueprint(file)
app.register_blueprint(page)
app.register_blueprint(permission)
app.register_blueprint(report)
app.register_blueprint(role)
app.register_blueprint(upload)
app.register_blueprint(user)


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
        session.pop('user_id')
    # Retorno de la función
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Ejecuta el servidor default port 5000
    # El debug en true permite ver cambios mientras se está editando
    csrf.init_app(app)
    db.init_app(app)

    email.init_app(app)
    with app.app_context():
        db.create_all()
        #insert_pages()
    #logging.basicConfig(filename='Log/myapp.log', level=logging.DEBUG)
    app.run(host="0.0.0.0", port=8000)

