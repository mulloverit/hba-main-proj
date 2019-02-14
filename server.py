"""Flask server for image differencing application"""
from datetime import datetime
from flask import Flask, request, jsonify, render_template, flash, redirect, session
import os
from PIL import Image

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
    username = request.form['username']
    password = request.form['password']

    # Check if username exists
    try:
        user = User.query.filter(User.username == username).one()

        # If Y, check that password is valid
        if password == user.password:

            session['username'] = username
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

        if db_check_if_user_exists(username):

            flash("Already a user. Please pick a unique username or sign in.")
            return redirect("/")

    except:

        db_add_new_user(username, email, password, fname, lname)

    return render_template("index.html")


@app.route("/upload-inputs", methods=['POST'])
def upload_check_inputs():
    """Handle initial image upload [no login required]."""

    try:
        
        username = session['username']
        user = User.query.filter(User.username == session['username']).one()
        # user_id = user.user_id

    except:

        username = "tmp"
        flash("Not logged in.")


    # retrieve images from page

    try:
        input_imgs_paths = []
        input_imgs = [request.files['img-1'], request.files['img-2']]
        
        ####################### THIS WORKS ########################
        username = "tmp"
        for img in input_imgs:
            mime = img.content_type
            print("OK", mime)
            key = username + "/" + img.filename.rsplit("/")[-1]
            print("######%%%%%%%%%%", img, "%%%%%%%%%###########")
            print("######%%%%%%%%%%", S3_BUCKET, "%%%%%%%%%###########")
            print("######%%%%%%%%%%", key, "%%%%%%%%%###########")
            print("######%%%%%%%%%%", mime, "%%%%%%%%%###########")


            upload_begin_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            
            s3.upload_fileobj(
                img,
                S3_BUCKET,
                key)
            
            upload_complete_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
            print("{}{}".format(S3_LOCATION, img.filename))
            print("WEEE")
            
            flash("Upload to S3 success")

        return redirect("/")

        ################# ^^^^^^^^^^^^^^^^^^^ ####################


        ########## do i want to keep this? ##########
            # img_path = save_input_img_to_tmp(img)
            ### save input img to tmp logic
        #     if allowed_file_formats(img.filename):
        #         img_name = secure_filename(img.filename)
        #         img_path = os.path.join(app.config['TMP_UPLOAD_FOLDER'], img_name)
        #         img.save(img_path)
        #         print(img_path)
        #         ###
        #     input_imgs_paths.append(img_path)


        
        # session['input_imgs_paths'] = input_imgs_paths

        return redirect("/upload-to-s3")
        

    except:
        flash("Please provide two valid files for upload.")
        return redirect("/")


# @app.route("/upload-to-s3")
# def upload_to_s3():
    
    
#     for img in session.get('input_imgs_paths'):
#         print (img)
        
#         upload_begin_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

#         # im_s3_url = upload_file_to_s3(img.filename, S3_BUCKET, user.username) # WORKING? PROB NOT
#         try:
#             #bucket_loc = S3_BUCKET + "/" + username
#             open_img = Image.open(img)
#             mimetype = Image.MIME[open_img.format]
#             key = username + "/" + open_img.filename.rsplit("/")[-1]
#             print("######%%%%%%%%%%", img, "%%%%%%%%%###########")
#             print("######%%%%%%%%%%", open_img, "%%%%%%%%%###########")
#             print("######%%%%%%%%%%", S3_BUCKET, "%%%%%%%%%###########")
#             print("######%%%%%%%%%%", key, "%%%%%%%%%###########")
#             print("######%%%%%%%%%%", mimetype, "%%%%%%%%%###########")

#             # filename, bucketname, keyname, 
#             s3.upload_fileobj(
#                 open_img,
#                 S3_BUCKET,
#                 key)

#             print("WEEE")
#             S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
#             print("{}{}".format(S3_LOCATION, img.filename))
#             flash("Upload to S3 success")
#             return redirect("/")

#         except:

#             flash("Error occurred while attempting upload")
#             return redirect("/")

# DATABASE MANIP - WORRY ABOUT AFTER S3 UPLOADS WORKING    
    # if im_s3_url: # If valid URL returned, add to db with upload completion time
    #     upload_complete_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    # else: # Otherwise, record a failure with timestamp and notify user
    #     upload_complete_datetime = ("FAILED AT " + datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    #     db_add_input_img(img,
    #                  user_id,
    #                  input_1,
    #                  input_2,
    #                  upload_begin_datetime,
    #                  upload_complete_datetime) 
    #     flash("Logging file to S3 failed.")

# HANDLING FOR WHEN A USER IS NOT LOGGED IN - PROB WANT TO CHANGE THIS LOGIC FROM local tmp dir to username=tmp
#     # If user not logged in, don't do any more work.
#         input_imgs_paths = []

#         for img in input_imgs:
#             img_path = save_input_img_to_tmp(img)
#             input_imgs_paths.append(img_path)

#         session['input_imgs_paths'] = input_imgs_paths

#         flash("Click diff button for result!")
    
#     return redirect("/")

@app.route("/submit-diff-request", methods=['POST'])
def diff_images():
    """Diff images [no login required]."""
    
    try:

        bool_img_path = create_boolean_diff(session.get('input_imgs_paths')[0], \
                                        session.get('input_imgs_paths')[1])
        session['bool_img_path'] = bool_img_path

        # if user is loggged in add to db?

    except:

        flash("Diff failed :(")

    return redirect("/")
    
@app.route("/upload-diff", methods=['POST'])
def upload_diff():
    """Upload diff to s3 for users who are logged in"""

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)