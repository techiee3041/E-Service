from flask import Flask, request, jsonify, redirect, url_for, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from ..app import app, db


class Trader(db.Model):
    __tablename__ = 'traders'

    trade_id = db.Column(db.Integer, primary_key=True)
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

    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=False)

    def __init__(self, full_name, email, phone_number, password):
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Category(db.Model):
    __tablename__ = 'category'

    cat_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)

    def __init__(self, category_name):
        self.category_name = category_name

class Product(db.Model):
    __tablename__ = 'product'

    pro_id = db.Column(db.Integer, primary_key=True)
    pro_name = db.Column(db.String(100), nullable=False)
    pro_dec = db.Column(db.String(300), nullable=False)
    filename = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, pro_name, pro_dec, filename):
        self.pro_name = pro_name
        self.pro_dec = pro_dec
        self.filename = filename
class Cords(db.Model):
    __tablename__ = 'cords'

    cord_id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float(100), nullable=False)
    longitude = db.Column(db.Float(100), nullable=False)

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude= longitude

