from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import os
from werkzeug.utils import secure_filename

def allowed_file_formats(filename):
    """Utility for checking uploaded image formats"""

    # Returns boolean (T/F) based on whether file ext exists AND is in allowed formats set
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_FORMATS

def save_input_img_to_tmp(img):
    """Utility to temporarily store input images for non-auth'd users"""

    if allowed_file_formats(img.filename):
        img_name = secure_filename(img.filename)
        img_path = os.path.join(app.config['TMP_UPLOAD_FOLDER'], img_name)
        img.save(img_path)
        return img_path
        #input_imgs_paths.append(img_path)

def save_bool_img_to_tmp(img_path):
    """Utility to temporarily store boolean images for non-auth'd users"""
    if allowed_file_formats(img_path):
        img_name = secure_filename(img_path).rsplit('.')
        tmp_path = os.path.join(app.config['TMP_BOOL_FOLDER'], img_name)
        img.save(tmp_path)

def connect_to_db(app):
    """Connect the database to Flask application"""
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///imgdiffs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

# Set up database and flask app 
db = SQLAlchemy()
app = Flask(__name__)
connect_to_db(app)
TMP_UPLOAD_FOLDER = "tmp/uploads/"
TMP_BOOL_FOLDER = "tmp/bools/"
ALLOWED_FORMATS = set(['png', 'jpg', 'jpeg', 'tif'])
app.config['TMP_UPLOAD_FOLDER'] = TMP_UPLOAD_FOLDER
# app.secret_key = os.environ.get("SECRET_KEY")

# AWS S3 specific environment variabls
S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
S3_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION = 'http://{}s3.amazonaws.com/'.format(S3_BUCKET)