from dotenv import load_dotenv
import os
import redis

load_dotenv() # take environment variables from .env.

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO= True
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
    
    # This sets the SQLALCHEMY_DATABASE_URI attribute to the string sqlite:///site.db. This URI is used by SQLAlchemy, the database toolkit for Flask, to specify the location of the SQLite database file named site.db.
    # This sets the SQLALCHEMY_TRACK_MODIFICATIONS attribute to False. This configuration option disables the modification tracking feature of SQLAlchemy, which can help improve performance.