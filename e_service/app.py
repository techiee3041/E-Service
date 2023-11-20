from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e-service.db'
app.secret_key = 'DOREEN_DANCAN'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'Doreen Nyaundi'
app.config['MAIL_PASSWORD'] = 'wxlgrivlnpfulihw'
app.config['MAIL_DEFAULT_SENDER'] = 'momanyinyaundis@gmail.com'

mail = Mail(app)


db = SQLAlchemy(app)