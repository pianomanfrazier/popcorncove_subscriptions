from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .authentication import requires_auth

# TODO: serve static files using WhiteNoise
app = Flask(__name__,
            static_folder='./dist/static',
            template_folder='./dist')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
