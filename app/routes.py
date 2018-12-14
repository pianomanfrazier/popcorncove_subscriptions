from app import app
from flask import render_template
from .authentication import requires_auth

@app.route('/')
@requires_auth
def index():
    return render_template('index.html') # this is a static file