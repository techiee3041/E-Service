from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from e_service.app import app, db
from haversine import haversine
from flask_login import current_user
from itsdangerous import TimedSerializer as Serializer


upload_folder = os.path.join(os.getcwd(), 'uploads')
# Create the upload folder if it doesn't exist
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
from e_service.models.data import Trader, User, Product, Category, UserLocation, TraderLocation, Admin, trader_product_association, trader_category_association # Import specific classes from data module

if isinstance(current_user, Trader):
    trader_id = current_user.trader_id
    # Rest of your code for traders
else:
    print("trader not found")
    # Handle the case for regular users


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
    categories = Category.query.all()

    if request.method == 'POST':
        pro_name = request.form['pro_name']
        pro_dec = request.form['pro_dec']
        pro_cont = request.form['pro_cont']
        category_id = request.form['category']

        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('list_files'))

        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('register_product'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Assuming you're using Flask-Login and the current_user is the logged-in trader
            new_product = Product(
                pro_name=pro_name,
                pro_dec=pro_dec,
                pro_cont=pro_cont,
                category_id=category_id,
                filename=filename
            )

            db.session.add(new_product)
            db.session.commit()

            # Now, associate the product with the current trader
            trader_id = current_user.trader_id
            association_entry = trader_product_association.insert().values(trader_id=trader_id, product_id=new_product.pro_id)
            db.session.execute(association_entry)
            db.session.commit()

            flash('Registration successful!', 'success')
            return redirect(url_for('trader_dashboard'))

    return render_template('product_registration.html', categories=categories)

# Helper function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
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
        user_id = current_user.id_user

        new_cords = UserLocation(latitude=latitude, longitude=longitude, user_id=user_id)

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

@app.route('/api/save_trader_coordinates', methods=['POST'])
def save_trader_coordinates():
    if request.method == 'POST':
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        user_id = current_user.trader_id

        new_cords = TraderLocation(latitude=latitude, longitude=longitude, trader_id=user_id)

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

@app.route('/fetch_user_and_trader_locations/<int:user_id>', methods=['GET'])
def fetch_user_and_trader_locations(user_id):
    user_location = UserLocation.query.filter_by(user_id=user_id).first()

    if user_location is None:
        return jsonify({'error': 'User location not found'})

    user_lat, user_lon = user_location.latitude, user_location.longitude
    nearby_traders = []

    for trader_location in TraderLocation.query.all():
        trader_lat, trader_lon = trader_location.latitude, trader_location.longitude
        distance = haversine((user_lat, user_lon), (trader_lat, trader_lon))

        if distance <= 5:
            trader_id = trader_location.trader_id
            trader_info = Trader.query.get(trader_id)

            # Fetch services offered by the trader
            trader_services_query = (
                db.session.query(Product)
                .join(trader_product_association)
                .filter_by(trader_id=trader_id)
            )

            trader_services = trader_services_query.all()

            trader_services_data = []

            for service in trader_services:
                # Access service attributes, handle None cases
                category_name = getattr(service.category, 'category_name', None)
                pro_name = getattr(service, 'pro_name', None)
                pro_dec = getattr(service, 'pro_dec', None)
                pro_cont = getattr(service, 'pro_cont', None)

                # Append service data to the list
                trader_services_data.append({
                    'category': category_name,
                    'description': pro_dec,
                    'product_name': pro_name,
                    'phone_number': pro_cont
                })

            nearby_traders.append({
                'trader_id': trader_id,
                'full_name': trader_info.full_name,
                'phone_number': trader_info.phone_number,
                'distance': distance,
                'services': trader_services_data
            })

    # Categorize traders
    categorized_traders = {}

    for trader in nearby_traders:
        trader_id = trader['trader_id']
        trader_name = trader['full_name']
        distance = trader['distance']

        for service in trader['services']:
            category = service['category']

            # Skip entries with None category
            if category is None:
                continue

            if category not in categorized_traders:
                categorized_traders[category] = []

            categorized_traders[category].append({
                'trader_id': trader_id,
                'trader_name': trader_name,
                'distance': distance,
                'category': category,
                'service': service,
            })

    # Return the categorized traders as a dictionary
    print(categorized_traders)
    return jsonify(categorized_traders)

@app.route('/edit/product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        # Update product information based on form data
        product.pro_name = request.form['pro_name']
        product.pro_dec = request.form['pro_dec']
        product.pro_cont = request.form['pro_cont']
        product.category_id = request.form['category']

        # Commit the changes to the database
        db.session.commit()

        flash('Product information updated successfully!', 'success')
        return redirect(url_for('trader_dashboard'))

    categories = Category.query.all()

    return render_template('edit_product.html', product=product, categories=categories)

# Delete Product
@app.route('/delete/product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    # Delete the product from the database
    db.session.delete(product)
    db.session.commit()

    flash('Product deleted successfully!', 'success')
    return redirect(url_for('trader_dashboard'))


@app.route('/fetch/products/<int:trader_id>')
def fetch_products(trader_id):
    # Assuming you have a relationship between Trader and Product in your models
    trader = Trader.query.get_or_404(trader_id)
    products = trader.services.all()  # Assuming 'products' is the relationship name

    return render_template('product_list.html', products=products, trader=trader)