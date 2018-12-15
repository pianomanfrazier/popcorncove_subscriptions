from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# TODO: serve static files using WhiteNoise
app = Flask(__name__,
            static_folder='./dist/static',
            template_folder='./dist')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .authentication import requires_auth
from app import routes, models
from .api import api

app.register_blueprint(api, url_prefix="/api/v1")
