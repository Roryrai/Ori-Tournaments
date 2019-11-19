from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_restful import Api
from app.api.user_resource import UserResource

app = Flask(__name__)


app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
bootstrap = Bootstrap(app)

from app.api import bp as api_bp
api = Api(app)
api.add_resource(UserResource, "/api/user/<string:user_id>")
app.register_blueprint(api_bp)

from app import models
