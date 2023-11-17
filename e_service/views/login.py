from flask import Flask, request, render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_wtf import FlaskForm
from wtforms.validators import Email, InputRequired
from wtforms import StringField, PasswordField, SubmitField
from e_service.app import app, db
from flask import abort


# Define User and Trader models in your 'data.py' file and import them here.
from e_service.models.data import User, Trader, Admin, Category

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Try loading a User first
    user = User.query.get(int(user_id))
    if user:
        return user

    # If User is not found, try loading a Trader
    trader = Trader.query.get(int(user_id))
    if trader:
        return trader

    # If Trader is not found, try loading an Admin
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin

    # If no user is found, return None
    return None
# Login Form

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


@app.route('/login/user', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user) # Log in the user
            print(current_user.is_authenticated)
            return redirect(url_for('user_dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('user_login.html', form=form)


@app.route('/login/trader', methods=['GET', 'POST'])
def login_trader():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        trader = Trader.query.filter_by(email=email).first()

        if trader and check_password_hash(trader.password_hash, password):
            login_user(trader)
            print(current_user.is_authenticated)
            print(current_user)
            return redirect(url_for('trader_dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('trader_login.html', form=form)

@app.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        admin = Admin.query.filter_by(email=email).first()

        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            print(current_user.is_authenticated)
            return redirect(url_for('admin_dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('admin_login.html', form=form)
    

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    if isinstance(current_user, User):
        print('Current user ID:', current_user.get_id())
        return render_template('user_dashboard.html', user_id=current_user.get_id())
    else:
        print('Current user is not logged in or not a User instance')
        # Handle the case where the user is not logged in or not a User instance
        # You might want to redirect them to the login page or handle it appropriately.
        return redirect(url_for('login_page'))



@app.route('/trader/dashboard')
@login_required
def trader_dashboard():
    if isinstance(current_user, Trader):
        trader_id = current_user.trader_id
        print(current_user.is_authenticated)
        return render_template('trader_dashboard.html', trader_id=trader_id, current_user=current_user)
    else:
        print('Current user is not logged in or not a Trader instance')
        # Handle the case where the user is not logged in or not a Trader instance
        # You might want to redirect them to the login page or handle it appropriately.
        return redirect(url_for('login_trader'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    categories = Category.query.all()
    return render_template('admin_dashboard.html', categories=categories)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
