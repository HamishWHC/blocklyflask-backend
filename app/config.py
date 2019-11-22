import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig():
    # Uncomment to force setting, even in CLI (test server on port 5000).
    # Displays stack traces in HTML page, can allow for code execution and is a security risk to enable.
    FLASK_DEBUG = True
    # Secret key for session encryption.
    SECRET_KEY = ""
    # Secret key for JWT Tokens.
    JWT_SECRET_KEY = ""

    # URI for database.
    SQLALCHEMY_DATABASE_URI = "postgresql://blocklyflask:verysecure@localhost:5432/blocklyflask"

    # Tracks modifications and emits signals. Disabled to reduce memory usage.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Logs ALL sql to stderr.
    SQLALCHEMY_ECHO = False

    # BlocklyFlask Configuration Options
