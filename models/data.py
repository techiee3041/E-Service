from flask import Flask, request, jsonify, redirect, url_for, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e-service.db'
app.secret_key = 'DOREEN_DANCAN'

db = SQLAlchemy(app)

class Trader(db.Model):
    __tablename__ = 'traders'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=False)

    def __init__(self, full_name, email, phone_number, business_name, password):
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number
        self.business_name = business_name
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    passwordd = db.Column(db.String(128), nullable=False)

    def __init__(self, full_name, email, phone_number, password):
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number
        self.set_password(password)

    def set_password(self, password):
        self.passwordd = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordd, password)

