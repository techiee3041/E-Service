from flask import render_template
from e_service.app import app


@app.route('/')
def index():
    return render_template('index.html')