"""Flask server for image differencing application"""
from io import StringIO
from datetime import datetime
from flask import Flask, request, jsonify, render_template, flash, redirect, session
import os
from PIL import Image
import uuid
from werkzeug.datastructures import FileStorage
import numpy as np
import cv2


from config import *
from database_manipulation import *
from diff_logic import *
from model import User, InputImage, DiffImage
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

        input_imgs = [request.files['img-1'], request.files['img-2']]
        
        # TO DO: add use of secure_filename and allowed_formats
        
        count = 0 # This is lame, but need some way to add img uuids to session uniquely?
        
        for img in input_imgs:
                    
            # Upload to S3
            img_uuid = str(uuid.uuid4())
            mime = img.content_type
            base_filename = img.filename.rsplit("/")[-1]
            key = username + "/" + img_uuid + "_" + base_filename
            upload_begin_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

            s3.upload_fileobj(
                img,
                S3_BUCKET,
                key,
                ExtraArgs={
                    'ContentType': mime
                    })
    
            upload_complete_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            S3_LOCATION = "http://{}.s3.amazonaws.com/".format(S3_BUCKET)
            img_s3_url = "{}{}".format(S3_LOCATION, key)
            
            print("UPLOADED: ", img_s3_url) # debugging help
            count += 1

            ## TRYING THIS OUT https://gist.github.com/mjul/32d697b734e7e9171cdb
            print("OK 1")
            in_memory_file = StringIO()
            print("OK 2")
            img.save(in_memory_file)
            print("OK 3")
            data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
            print("OK 4")
            color_image_flag = 1
            print("OK 5")
            img = cv2.imdecode(data, color_image_flag)
            print("OK 6")


        print("INPUT IMGS LIST: ", input_imgs)
        flash("Upload to S3 a success!")
        
        

        return redirect("/")

    except:

        flash("Please provide two valid files for upload.")
        
        return redirect("/")


### Where/when to add image to database with appropriate metadata?
# # Images are corrupted when going to S3 if opened before uploading
            # # But image also can't be opened _after_ being uploaded to S3
            # # Thinking I'll need to abstract the addition to database away from here
            # # and download file from s3 for database addition?? How else to get metadata?
            # # open image, grab metadata, close image
            # im = Image.open(img)
            # img_size_x = im.size[0]
            # img_size_y = im.size[1]
            # img_format = im.format
            # img_mode = im.mode
            # im.close()
            
            # image_database_record = db_add_input_img(user_id,
            #                              img_size_x,
            #                              img_size_y,
            #                              img_format,
            #                              img_mode,
            #                              img_s3_url,
            #                              upload_begin_datetime,
            #                              upload_complete_datetime,
            #                              img_uuid)

            # print("Added to database with UUID: ", image_database_record.im_uuid)
            # image_session_key = ('Image_' + str(count) + '_uuid')
            # session[image_session_key] = image_database_record.im_uuid
            # print(session[image_session_key])
            
@app.route("/submit-diff-request", methods=['POST'])
def diff_images():
    """Diff images [no login required]."""
    
    try:
        
        print("OK 1")
        print(session['Image_1_uuid'])
        image_1_row = InputImage.query.filter(InputImage.im_uuid == session['Image_1_uuid']).first()
        image_2_row = InputImage.query.filter(InputImage.im_uuid == session['Image_2_uuid']).first()

        print("OK 2")
        image_2_s3_url = image_1_row.im_s3_url
        image_2_s3_url = image_2_row.im_s3_url

        # This is brittle - to do: split on something else or store Key separate from Url in db
        image_key_1 = image_2_s3_url.split("s3.amazonaws.com")[-1]
        image_key_2 = image_2_s3_url.split("s3.amazonaws.com")[-1]
        
        print("OK 3")
        print(image_key_1)
        print(image_key_2)
        
        print("OK 4")
        image_keys = [image_key_1, image_key_2]
        files = []
        
        print("OK 5")
        for image_key in image_keys:
            
            filename = image_key.split('/')[-1]
            print("OK 6")
            print(s3_dl, S3_BUCKET, image_key, filename)

            try:
                s3_dl.Bucket(S3_BUCKET).download_file(image_key, filename)
            
            except botocore.exceptions.ClientError as e:
               if e.response['Error']['Code'] == "404":
                   print("The object does not exist.")
               else:
                   raise

            print("OK 7")
            files.append(filename)

        print("OK 8")
        bool_img_path = create_boolean_diff(files[0], files[1])
        print("OK 9")

        #session['bool_img_path'] = bool_img_path

    except:

        flash("Diff failed :(")

    return redirect("/")
    
@app.route("/upload-diff", methods=['POST'])
def upload_diff():
    """Upload diff to s3 for users who are logged in"""

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)