from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
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
    return User.query.get(int(user_id))
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
            user.authenticated = True
            login_user(user)  # Log in the user
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
            return redirect(url_for('admin_dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('admin_login.html', form=form)

class EditCategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[InputRequired()])
    submit = SubmitField('Save Changes')
    
@app.route('/edit_category/<int:cat_id>', methods=['GET', 'POST'])
def edit_category(cat_id):
    category = Category.query.get_or_404(cat_id)
    form = EditCategoryForm(obj=category)

    if form.validate_on_submit():
        form.populate_obj(category)
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_dashboard.html', form=form, category=category)


@app.route('/user/dashboard')
#@login_required
def user_dashboard():
    return render_template('user_dashboard.html', current_user=current_user)


@app.route('/trader/dashboard')
#@login_required
def trader_dashboard():
    return render_template('trader_dashboard.html')

@app.route('/admin/dashboard')
#@login_required
def admin_dashboard():
    categories = Category.query.all()
    form = EditCategoryForm()
    return render_template('admin_dashboard.html', categories=categories, form=form)


@app.route('/logout')
#@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
