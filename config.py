import os

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