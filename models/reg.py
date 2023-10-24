from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e-service.db'
app.secret_key = 'DOREEN_DANCAN'

db = SQLAlchemy(app)

# Define User and Trader models in your 'data.py' file and import them here.
from data import User, Trader

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registration Form
class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    phone_number = StringField('Phone Number', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Register')

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

@app.route('/register/user', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        phone_number = form.phone_number.data
        password = form.password.data
        password_confirm = form.password_confirm.data

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

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login_user'))

    return render_template('registration_user.html', form=form)

@app.route('/register/trader', methods=['GET', 'POST'])
def register_trader():
    form = RegistrationForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        phone_number = form.phone_number.data
        password = form.password.data
        password_confirm = form.password_confirm.data

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
            password=password
        )

        db.session.add(new_trader)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login_trader'))

    return render_template('registration_trader.html', form=form)

@app.route('/login/user', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('user_dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('login_user.html', form=form)

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

    return render_template('login_trader.html', form=form)

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    return "User Dashboard"

@app.route('/trader/dashboard')
@login_required
def trader_dashboard():
    return "Trader Dashboard"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

