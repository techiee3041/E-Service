from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from e_service.app import app, db



app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

from e_service.models.data import Trader, User, Product, Category, Cords, Admin # Import specific classes from data module

@app.route('/register/trader', methods=['GET', 'POST'])
def register_trader():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        business_name = request.form['business_name']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # Check if the passwords match
        if password != password_confirm:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('register_trader'))

        existing_trader = Trader.query.filter_by(email=email).first()
        if existing_trader:
            flash('Email address is already registered.', 'danger')
            return redirect(url_for('register_trader'))

        new_trader = Trader(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            business_name=business_name,
            password=password
        )

        db.session.add(new_trader)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login_trader'))

    return render_template('registration.html')

@app.route('/register/user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # Check if the passwords match
        if password != password_confirm:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('register_user'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address is already registered.', 'danger')
            return redirect(url_for('register_user'))

        new_user = User(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password
        )
        print(new_user.password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('user_login'))

    return render_template('registration_user.html')

@app.route('/register/product', methods=['GET', 'POST'])
def register_product():
    categories = Category.query.all()  # Fetch all categories from the database

    if request.method == 'POST':
        pro_name = request.form['pro_name']
        pro_dec = request.form['pro_dec']
        category_id = request.form['category']  # Get the selected category ID
        
        UPLOAD_FOLDER = 'uploads'
        if not os.path.exists(UPLOAD_FOLDER):
             os.makedirs(UPLOAD_FOLDER)

        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('list_files'))

        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('list_files'))

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_product = Product(
                pro_name=pro_name,
                pro_dec=pro_dec,
                filename=filename,
                #pro_id=category_id  # Assign the selected category ID
            )

            db.session.add(new_product)
            db.session.commit()

            flash('Registration successful!', 'success')
            return redirect(url_for('trader_dashboard'))

    return render_template('product_registration.html', categories=categories)

@app.route('/register/category', methods=['POST'])
def register_category():
    category_name = request.form['category_name']

    existing_category = Category.query.filter_by(category_name=category_name).first()

    if existing_category:
        flash('Category already exists!', 'danger')
    else:
        new_category = Category(category_name=category_name)
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully!', 'success')

    return redirect(url_for('admin_dashboard'))


@app.route('/register/admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        full_name=request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # Check if the passwords match
        if password != password_confirm:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('register_admin'))

        existing_admin = Admin.query.filter_by(email=email).first()
        if existing_admin:
            flash('Email address is already registered.', 'danger')
            return redirect(url_for('register_admin'))

        new_admin = Admin(
            full_name=full_name,
            email=email,
            password=password
        )

        db.session.add(new_admin)
        db.session.commit()

        flash('Admin registration successful!', 'success')
        return redirect(url_for('login_admin'))

    return render_template('registration_admin.html')


@app.route('/api/save_coordinates', methods=['POST'])
def save_coordinates():
    if request.method == 'POST':
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        new_cords = Cords(latitude=latitude, longitude=longitude)

        db.session.add(new_cords)
        db.session.commit()

        response = {
            'message': 'Coordinates saved successfully',
            'latitude': latitude,
            'longitude': longitude
        }

        return jsonify(response), 200
    else:
        response = {
            'message': 'Invalid request method. Use POST.'
        }
        return jsonify(response), 405