from app import app
from flask import render_template
from .authentication import requires_auth

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@requires_auth
def index(path):
    return render_template('index.html') # this is a static file