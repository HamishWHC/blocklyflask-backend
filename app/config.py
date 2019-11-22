import os
from configparser import ConfigParser

BASEDIR = os.path.abspath(os.path.dirname(__file__))

private_ini = ConfigParser()
private_ini.read('private.ini')

class BaseConfig():
    # Uncomment to force setting, even in CLI (test server on port 5000).
    # Displays stack traces in HTML page, can allow for code execution and is a security risk to enable.
    FLASK_DEBUG = True
    # Secret key for session encryption.
    SECRET_KEY = private_ini["dev"]["session_secret"]
    # Secret key for JWT Tokens.
    JWT_SECRET_KEY = private_ini["dev"]["jwt_secret"]

    # URI for database.
    SQLALCHEMY_DATABASE_URI = private_ini["dev"]["sqlalchemy_db_uri"]

    # Tracks modifications and emits signals. Disabled to reduce memory usage.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Logs ALL sql to stderr.
    SQLALCHEMY_ECHO = False

    # BlocklyFlask Configuration Options
