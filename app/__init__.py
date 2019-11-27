from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_restful import Api
from flask_marshmallow import Marshmallow

app = Flask(__name__)


app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
bootstrap = Bootstrap(app)
marshmallow = Marshmallow(app)

from app.models import bp as models_bp
from app.schemas import bp as schemas_bp
app.register_blueprint(models_bp)
app.register_blueprint(schemas_bp)

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix="/api")
