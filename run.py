from e_service.app import app, db
import e_service.views.index
from e_service.views.login import *
from e_service.views.registration import *
from e_service.views.forgot_password import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5002)
