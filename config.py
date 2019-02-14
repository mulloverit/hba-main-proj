from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import os


def connect_to_db(app):
    """Connect the database to Flask application"""
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///imgdiffs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


# Set up database and flask app 
db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
connect_to_db(app)


# AWS S3 specific environment variabls
S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
S3_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION = 'http://{}s3.amazonaws.com/'.format(S3_BUCKET)