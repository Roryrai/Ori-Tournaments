import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Database config
    SQLALCHEMY_DATABASE_URI = "postgres://" + \
        os.environ.get("DATABASE_USERNAME") + ":" + \
        os.environ.get("DATABASE_PASSWORD") + "@" + \
        os.environ.get("DATABASE_URL") + "/" + \
        os.environ.get("DATABASE_NAME") \
        if os.environ.get("DATABASE_URL") and os.environ.get("DATABASE_USERNAME") and os.environ.get("DATABASE_PASSWORD") \
        else "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key config
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # JWT config
    JWT_AUTH_HEADER_PREFIX = os.environ.get("JWT_AUTH_HEADER_PREFIX")
    JWT_EXPIRATION_DELTA = timedelta(seconds=int(os.environ.get("JWT_EXPIRATION_DELTA")))
