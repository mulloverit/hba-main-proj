"""Flask server for image differencing application"""
from io import StringIO, BytesIO
from datetime import datetime
from flask import Flask, request, jsonify, render_template, flash, redirect, session
import os
from PIL import Image
import uuid
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage

from config import *
from database_manipulation import *
from diff_logic import *
from model import User, InputImage, DiffImage, ImageClass, UserClass
from s3_manipulation import upload_file_to_s3
from utils import user_sign_in, user_registration_new


app.secret_key = "what"


@app.route("/")
def show_index():
        """Index/homepage"""

        session['username'] = 'tmp'
        return render_template("index.html")


@app.route("/sign-in", methods=['POST'])
def sign_in():
    """Log in an existing user"""

    message = user_sign_in(request.form['username'], request.form['password'])

    if "Success" in message:
        session['username'] = request.form['username']

    flash (message)

    return render_template("index.html")


@app.route("/register-new", methods=['POST'])
def register_user():
    """Add a new user to database"""

    message = user_registration_new(request.form['username'], request.form['password'],
                     request.form['email'], request.form['fname'], request.form['lname'])
    
    flash (message)

    return render_template("index.html")


@app.route("/upload-inputs", methods=['POST'])
def upload_inputs():
    """Handle initial image upload [no login required]."""

    username, user_id = current_user()

    try:
        
        session['tmp_request_image_files'] = []
        session['request_image_ids'] = []

        for request_image in [request.files['img-1'], request.files['img-2']]:

            tmp_path = 'tmp/uploads/{}_{}'.format(username, request_image.filename)
            
            request_image.save(tmp_path)

            request_image_object = ImageClass(request_image, tmp_path, username)
            request_image_object.upload_to_s3(S3_BUCKET)
            request_image_object.add_to_database(user_id)
            
            session['tmp_request_image_files'].append(tmp_path)
            session['request_image_ids'].append(request_image_object.image_id)

        flash("Upload to S3 a success!")
        
        return redirect("/")

    except:

        flash("Please provide two valid files for upload.")
        
        return redirect("/")


@app.route("/submit-diff-request", methods=['POST'])
def diff_images():
    """Diff images from local dir [no s3 and no login required]."""
    
    username, user_id = current_user()

    try:

        boolean_diff_path = create_boolean_diff(
                                        session['tmp_request_image_files'][0],
                                        session['tmp_request_image_files'][1]
                                        )
        
        difference_image = ImageClass(boolean_diff_path, boolean_diff_path, username) # wants path not PIL object
        difference_image.upload_to_s3(S3_BUCKET)
        difference_image.add_to_database(user_id, input_image_ids=session['request_image_ids'])

        flash("Diff succeeded.")

    except:

        flash("Diff failed :(")

    return redirect("/")
    

if __name__ == "__main__":
    app.run(debug=True)