from e_service.app import app, db, mail
from e_service.views.index import *
from e_service.views.login import *
from e_service.views.registration import *
from e_service.views.forgot_password import reset_request_trader, reset_password_trader, reset_request_user, reset_password_user

# Add password reset routes to the Flask application
app.add_url_rule("/reset_password_trader", methods=['GET', 'POST'], view_func=reset_request_trader)
app.add_url_rule("/reset_password_trader/<token>", methods=['GET', 'POST'], view_func=reset_password_trader)
app.add_url_rule("/reset_password_user", methods=['GET', 'POST'], view_func=reset_request_user)
app.add_url_rule("/reset_password_user/<token>", methods=['GET', 'POST'], view_func=reset_password_user)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5004)
