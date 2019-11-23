from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_restful import Api

app = Flask(__name__)


app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
bootstrap = Bootstrap(app)

from app.models import bp as models_bp
from app.schemas import bp as schemas_bp
app.register_blueprint(models_bp)
app.register_blueprint(schemas_bp)

from app.api import bp as api_bp
from app.api.user_resource import UserResource

api = Api(app)
api.add_resource(UserResource, "/api/user/<string:user_id>")
app.register_blueprint(api_bp)
