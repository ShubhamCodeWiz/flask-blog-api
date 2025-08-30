# config.py
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-duper-secret-key-change-me'
    
    # UPDATED: Read the database URI from an environment variable
    # If the variable is not set, it will fall back to the old SQLite config.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
# NEW: Create a new config class for testing
class TestConfig(Config):
    # Use a separate file for the test database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    # Enable Flask's testing mode. This makes error handling easier in tests.
    TESTING = True