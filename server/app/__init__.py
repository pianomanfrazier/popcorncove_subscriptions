from flask import Flask, render_template
from .authentication import requires_auth

# TODO: serve static files using WhiteNoise
app = Flask(__name__,
            static_folder='./dist/static',
            template_folder='./dist')

@app.route('/')
@requires_auth
def index():
    return render_template('index.html') # this is a static file
