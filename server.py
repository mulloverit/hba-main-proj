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
from model import User, InputImage, DiffImage, ImageClass
from s3_manipulation import upload_file_to_s3

app.secret_key = "what"

@app.route("/")
def show_index():
        """Index/homepage"""

        return render_template("index.html")

@app.route("/sign-in", methods=['POST'])
def sign_in():
    """Log in an existing user"""

    # Retrieve POSTed form data
    request_username = request.form['username']
    request_password = request.form['password']

    # Check if username exists
    try:
        user = User.query.filter(User.username == request_username).one() # THIS IS NOT WORKING 

        # If Y, check that password is valid
        if user.password == request_password:
            # could get rid of lines 27-28 and do:
        # if user.password == request.form['password']

            # could create helper function in place of these lines
            # add_to_session(key, value)
            # sign_in_user(user) # _not_ a class/instance method -- goes under "utils" bc it is glue logic rather than user specifc
            # Session.sign_in_user(user) 
            session['username'] = request_username
            session['user_id'] = user.user_id
            flash("Successfully logged in.")

    # If N, notify user of failed login
    except:

        flash("Login failed.")
        return redirect("/")

    return render_template("index.html")

@app.route("/register-new", methods=['POST'])
def register_user():
    """Add a new user to database"""

    # Retrieve POSTed form data
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    fname = request.form['fname']
    lname = request.form['lname']
    
    try:
        # if User.exists(username) # make class method
        if db_check_if_user_exists(username):

            flash("Already a user. Please pick a unique username or sign in.")
            
            return redirect("/")

    except:
    
        db_add_new_user(username, email, password, fname, lname)
        # db_add_new_user(username, email, request.form['password'],
        #                request.form['fname'], request.form['lname']) # fname --> first_name etc

    return render_template("index.html")


@app.route("/upload-inputs", methods=['POST'])
def upload_inputs():
    """Handle initial image upload [no login required]."""

    try:
        # abstract this to a method called current_user -- ths would go into utils/session helpers where
        # you also have sign_in and sign_out.
        # if current_user:
            # replaces this whole try/except 
        username = session['username']
        user = User.query.filter(User.username == session['username']).one()
        user_id = user.user_id
        
    except:

        # Maintain a db username item for "tmp" at loc user_id = 1
        username = "tmp"
        user_id = 1

    try:
        
        session['tmp_request_image_files'] = []
        session['request_image_uuids'] = []

        for request_image in [request.files['img-1'], request.files['img-2']]:

            tmp_path = 'tmp/uploads/{}_{}'.format(username, request_image.filename)
            
            request_image.save(tmp_path)

            request_image_object = ImageClass(request_image, tmp_path, username)
            request_image_object.upload_to_s3(S3_BUCKET)
            request_image_object.add_to_database(user_id)
            
            session['tmp_request_image_files'].append(tmp_path)
            session['request_image_uuids'].append(request_image_object.uuid)

        flash("Upload to S3 a success!")
        
        return redirect("/")

    except:

        flash("Please provide two valid files for upload.")
        
        return redirect("/")
            
@app.route("/submit-diff-request", methods=['POST'])
def diff_images():
    """Diff images from local dir [no s3 and no login required]."""
    
    try:
        # abstract this to a method called current_user -- ths would go into utils/session helpers where
        # you also have sign_in and sign_out.
        # if current_user:
            # replaces this whole try/except 
        username = session['username']
        user = User.query.filter(User.username == session['username']).one()
        user_id = user.user_id
        
    except:

        # Maintain a db username item for "tmp" at loc user_id = 1
        username = "tmp"
        user_id = 1

    try:

        boolean_diff_path = create_boolean_diff(
                                        session['tmp_request_image_files'][0],
                                        session['tmp_request_image_files'][1]
                                        )
        
        difference_image = ImageClass(boolean_diff_path, boolean_diff_path, username) # wants path not PIL object
        difference_image.upload_to_s3(S3_BUCKET)
        difference_image.add_to_database(user_id, input_images=session['request_image_uuids'])

        flash("Diff succeeded.")

    except:

        flash("Diff failed :(")

    return redirect("/")
    


if __name__ == "__main__":
    app.run(debug=True)