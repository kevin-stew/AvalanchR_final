from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from config import Config
from .helpers import JSONEncoder
from .site.routes import site
from .api.routes import api
from .authentication.routes import auth
from .models import db as root_db, login_manager, ma

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(api)
app.register_blueprint(site)
app.register_blueprint(auth)

root_db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login' #specify the page rendered for non-authed users
ma.init_app(app)
migrate = Migrate(app, root_db)

CORS(app)
app.json_encoder = JSONEncoder