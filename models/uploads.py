from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful_fileupload import FileUpload
from werkzeug.utils import secure_filename
import os

app = Flask(__name)
app.secret_key = 'your_secret_key'  # Set a secret key for session management and flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'  # Define a folder for file uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Set a max file size (e.g., 16MB)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Create a File model for database storage
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    filename = db.Column(db.String(255), unique=True, nullable=False)
    trader_id = db.Column(db.Integer, nullable=False)

    def __init__(self, name, filename, trader_id):
        self.name = name
        self.filename = filename
        self.trader_id = trader_id

# Create a TraderDetails model for trader-specific details
class TraderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    details = db.Column(db.String(255))
    trader_id = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, name, details, trader_id):
        self.name = name
        self.details = details
        self.trader_id = trader_id

# Create a FileSchema for serialization/deserialization
class FileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'filename', 'trader_id')

file_schema = FileSchema()
files_schema = FileSchema(many=True)

# Initialize file upload extension
file_upload = FileUpload()

# Sample traders (you should use proper authentication)
traders = {'trader1': 1, 'trader2': 2}

def get_current_trader_id():
    username = session.get('username')
    return traders.get(username, None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
    else:
        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'error')
        else:
            trader_id = get_current_trader_id()
            if trader_id is None:
                flash('Unauthorized', 'error')
            else:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_file = File(name=file.filename, filename=filename, trader_id=trader_id)
                try:
                    db.session.add(new_file)
                    db.session.commit()
                    flash('File uploaded successfully', 'success')
                except Exception as e:
                    flash('File upload failed', 'error')
    return redirect(url_for('list_files'))

@app.route('/files')
def list_files():
    trader_id = get_current_trader_id()
    if trader_id is None:
        flash('Unauthorized', 'error')
        return redirect(url_for('login'))

    trader_files = File.query.filter_by(trader_id=trader_id).all()
    return render_template('trader_dashboard.html', trader_files=trader_files)

@app.route('/upload_form', methods=['GET', 'POST'])
def upload_form():
    if request.method == 'POST':
        name = request.form['name']
        details = request.form['details']
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            trader_id = get_current_trader_id()
            if trader_id is None:
                flash('Unauthorized', 'error')
                return redirect(url_for('login'))
            new_file = File(name=file.filename, filename=filename, trader_id=trader_id)
            try:
                db.session.add(new_file)
                db.session.commit()
                flash('File uploaded successfully', 'success')
            except Exception as e:
                flash('File upload failed', 'error')
                return redirect(url_for('upload_form'))

            trader_details = TraderDetails.query.filter_by(trader_id=trader_id).first()
            if trader_details is None:
                trader_details = TraderDetails(trader_id=trader_id, name=name, details=details)
                db.session.add(trader_details)
            else:
                trader_details.name = name
                trader_details.details = details
            db.session.commit()
            flash('Trader details updated', 'success')

    return render_template('upload_form.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

