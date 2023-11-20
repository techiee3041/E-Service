from flask import render_template, url_for, flash, redirect, request
from flask_mail import Message
from e_service.models.data import Trader, User  # Import your Trader and User models
from e_service.app import app, db, mail
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, InputRequired
from itsdangerous import TimedSerializer as Serializer

class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Reset Password')

# Assuming you have the necessary configurations for Flask-Mail and other dependencies

@app.route("/reset_password_trader", methods=['GET', 'POST'])
def reset_request_trader():
    form = ResetPasswordForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        trader = Trader.query.filter_by(email=email).first()

        if trader:
            token = trader.generate_reset_token()  # Assuming you have the method in your Trader model
            reset_link = url_for('reset_password_trader', token=token, _external=True)
            msg = Message('Password Reset Request', sender='meservice254@gmail.com', recipients=[email])
            msg.body = f'''To reset your password, visit the following link:
                         {reset_link}

                         If you did not make this request, ignore this email.
                         '''
            mail.send(msg)  # Assuming you have the Flask-Mail instance named 'mail'
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('login'))  # Assuming you have a route for trader login
        else:
            flash('Email does not exist in our database. Please register.', 'danger')

    return render_template('reset_request_trader.html', form=form)

@app.route("/reset_password_trader/<token>", methods=['GET', 'POST'])
def reset_password_trader(token):
    trader = Trader.verify_reset_token(token)  # Assuming you have the method in your Trader model
    if trader is None:
        flash('Invalid or expired token. Please try again.', 'warning')
        return redirect(url_for('reset_request_trader'))

    # Handle password reset form submission
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        trader.set_password(new_password)  # Assuming you have the method in your Trader model
        db.session.commit()
        flash('Your password has been reset!', 'success')
        return redirect(url_for('login'))  # Assuming you have a route for trader login

    return render_template('reset_password_trader.html')  # Create this template similar to reset_password.html

@app.route("/reset_password_user", methods=['GET', 'POST'])
def reset_request_user():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.generate_reset_tokens()  # Assuming you have the method in your User model
            reset_link = url_for('reset_password_user', token=token, _external=True)
            msg = Message('Password Reset Request', sender='meservice254@gmail.com', recipients=[email])
            msg.body = f'''To reset your password, visit the following link:
                         {reset_link}

                         If you did not make this request, ignore this email.
                         '''
            mail.send(msg)  # Assuming you have the Flask-Mail instance named 'mail'
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('user_login'))  # Assuming you have a route for user login
        else:
            flash('Email does not exist in our database. Please register.', 'danger')

    return render_template('reset_request_user.html')  # Create this template similar to reset_request.html

@app.route("/reset_password_user/<token>", methods=['GET', 'POST'])
def reset_password_user(token):
    user = User.verify_reset_tokens(token)  # Assuming you have the method in your User model
    if user is None:
        flash('Invalid or expired token. Please try again.', 'warning')
        return redirect(url_for('reset_request_user'))

    # Handle password reset form submission
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        user.set_password(new_password)  # Assuming you have the method in your User model
        db.session.commit()
        flash('Your password has been reset!', 'success')
        return redirect(url_for('user_login'))  # Assuming you have a route for user login

    return render_template('reset_password_user.html')  

