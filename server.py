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
        user = User.query.filter(User.username == request_username).one()

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

        request_file_1 = request.files['img-1']
        request_file_2 = request.files['img-2']

        tmp_path_upload_1 = 'tmp/uploads/{}_{}'.format(username, request_file_1.filename)
        tmp_path_upload_2 = 'tmp/uploads/{}_{}'.format(username, request_file_2.filename)

        locally_saved_user_upload_1 = request_file_1.save(tmp_path_upload_1)
        locally_saved_user_upload_2 = request_file_2.save(tmp_path_upload_2)
        
        # TO DO: add use of secure_filename and allowed_formats

        input_image_1 = ImageClass(request_file_1, tmp_path_upload_1, username)
        input_image_2 = ImageClass(request_file_2, tmp_path_upload_1, username)

        input_image_1.upload_to_s3(S3_BUCKET)
        input_image_2.upload_to_s3(S3_BUCKET)
        
        flash("Upload to S3 a success!")
        
        return redirect("/")

    except:

        flash("Please provide two valid files for upload.")
        
        return redirect("/")
            
@app.route("/submit-diff-request", methods=['POST'])
def diff_images():
    """Diff images [no login required]."""
    
    try:
        
        # is this going to be local or are inputs from s3?
        create_boolean_diff(input_image_1.filename, input_image_2.filename)


        # Perform the image differencing operation
        username = session['username']
        image_1_s3_key = session['Image_1_s3_key']
        image_2_s3_key = session['Image_2_s3_key']
        image_keys = [image_1_s3_key, image_2_s3_key]
        
        files = []

        for image_key in image_keys:
            
            filename = image_key.split('/')[-1]
            file_location = 'tmp/downloads/' + filename
        
            try:
                s3_dl.Bucket(S3_BUCKET).download_file(image_key, file_location)
            
            except botocore.exceptions.ClientError as e:
               if e.response['Error']['Code'] == "404":
                   print("The object does not exist.")
               else:
                   raise

            files.append(file_location)

        bool_img_local_path = create_boolean_diff(files[0], files[1])

        session['bool_img_local_path'] = bool_img_local_path
        session['input_images_local_paths'] = files

        flash("Diff succeeded.")

    except:

        flash("Diff failed :(")

    return redirect("/")
    
@app.route("/save-image-records-to-database", methods=['POST'])
def save_image_records_to_database():
    """Save record of input images and diff to database"""

    ##########  THIS TRY/EXCEPT GRABBING USERNAME AND USER_ID IS  ##############
    ##### REPETITIVE (SAME AS UPLOAD INPUT ROUTE) IT WILL BE ABSTRACTED ########

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

    ############################################################################


    input_image_1, input_image_2 = session['input_images_local_paths'][0], session['input_images_local_paths'][1]
    boolean_output_image = session['bool_img_local_path']

    # Add records of input images to database table
    count = 1
    for image in session['input_images_local_paths']:

        image_count_string = ('Image_' + str(count))
        img_s3_key = session[image_count_string + '_s3_key']
        upload_begin_datetime = session[image_count_string + '_upload_begin_datetime']
        upload_complete_datetime = session[image_count_string + '_upload_begin_datetime']
        img_uuid = session[image_count_string + '_uuid']

        im = Image.open(image)
        img_size_x = im.size[0]
        img_size_y = im.size[1]
        img_format = im.format
        img_mode = im.mode
        im.close()
        

        image_database_record = db_add_input_img(user_id,
                                     img_size_x,
                                     img_size_y,
                                     img_format,
                                     img_mode,
                                     img_s3_key,
                                     upload_begin_datetime,
                                     upload_complete_datetime,
                                     img_uuid)

        image_session_uuid_key = ('Image_' + str(count) + '_uuid')
        image_session_ID_key = ('Image_' + str(count) + '_IMGID')
        print(image_session_ID_key)
        session[image_session_uuid_key] = image_database_record.im_uuid
        session[image_session_ID_key] = image_database_record.im_id
        print(session[image_session_uuid_key])
        print(session[image_session_ID_key])
        print("InputImage added to database with UUID: ", image_database_record.im_uuid)
        count += 1

    # Add boolean record to database
    im = Image.open(boolean_output_image)
    diff_size_x = im.size[0]
    diff_size_y = im.size[1]
    diff_format = im.format
    diff_mode = im.mode
    im.close()

    input_diff_id_1 = session['Image_1_IMGID']
    input_diff_id_2 = session['Image_2_IMGID']

    diff_database_record = db_add_diff_img(user_id,
                                 input_diff_id_1,
                                 input_diff_id_2,
                                 diff_size_x,
                                 diff_size_y,
                                 diff_format,
                                 diff_mode,
                                 img_s3_key, #### THIS IS WRONG - currently inherits from InputImage 2
                                 upload_begin_datetime,
                                 upload_complete_datetime,
                                 diff_uuid) #### THIS IS WRONG - currently inherits from InputImage 2

    session['Boolean_uuid'] = diff_database_record.diff_uuid
    print(session['Boolean_uuid'])
    print("Diff added to database with UUID: ", diff_database_record.diff_uuid)


    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)