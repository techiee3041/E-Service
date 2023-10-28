from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField, PasswordField, SubmitField
from e_service.app import app, db

# Define User and Trader models in your 'data.py' file and import them here.
from e_service.models.data import User, Trader

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# Login Form


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
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
            login_user(user)  # Log in the user
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

        if trader and check_password_hash(trader.password, password):
            login_user(trader)
            return redirect(url_for('trader_dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('trader_login.html', form=form)


@app.route('/user/dashboard')
#@login_required
def user_dashboard():
    return render_template('user_dashboard.html')


@app.route('/trader/dashboard')
@login_required
def trader_dashboard():
    return render_template('trader_dashboad.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
