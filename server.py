"""Flask server for image differencing application"""
from datetime import datetime
from flask import Flask, request, jsonify, render_template, flash, redirect, session
from PIL import Image

from config import *
from s3_manipulation import upload_file_to_s3
from model import User, InputImage, DiffImage

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/upload-inputs", methods=['POST'])
def upload_input_images():
    """Handle initial image upload [no login required]."""

    # retrieve images from page
    try:
        # img_1 = request.files['img-1']
        # img_2 = request.files['img-2']
        input_imgs = [request.files['img-1'], request.files['img-2']]

    except:
        flash("Please provide two valid files for upload.")
        return

    try:
           username = session['username'] 
           user = User.query.filter(User.username == session['username']).one()
           user_id = user.user_id

        for img in input_imgs:
        
            upload_begin_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            im_s3_url = upload_file_to_s3(img, S3_BUCKET, user.username) 
        
            if im_s3_url: # If valid URL returned, add to db with upload completion time
                upload_complete_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
            else: # Otherwise, record a failure with timestamp and notify user
                upload_complete_datetime = ("FAILED AT " + datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

            # from database_manipulation
            db_add_input_img(user_id,
                             input_1,
                             input_2,
                             upload_begin_datetime,
                             upload_complete_datetime) 

            flash("Logging file to S3 failed.")

    # If not logged in, just diff. No s3, no db.
    except:
        
        flash("Not logged in - uploaded images will not persist if page refreshed.")

    flash("Upload success!") # PERHAPS NEEDS TO BE MOVED 
    
    return redirect("/")

# @app.route("/submit-diff-request", methods="[POST]")
# def diff_images():
#     """Diff images [no login required]."""

#     # recognize action when user clicks "diff" button
#     # grab records from database and files from s3
#     # send two images to image diffing function --> send to server for diff-ing??
#     # return/render diff'd image

# @app.route("/upload-diff", methods="[POST]")
# add to html: IF logged in, save diff to s3 for later access


@app.route("/")
def show_index():
        """Index/homepage"""

        return render_template("index.html")

@app.route("/", methods=['POST'])
def sign_in():
    """Log in an existing user"""

    # Retrieve POSTed form data
    username = request.form['username']
    password = request.form['password']

    # Check if username exists
    try:
        user = User.query.filter(User.username == username).one()

        # If Y, check that password is valid
        if user.password == password:

            session['username'] = username
            flash("Successfully logged in")

    # If N, notify user of failed login
    except:
        flash("Login failed")

    return render_template("index.html")

@app.route("/", methods=['POST'])
def register_user():
    """Add a new user to database"""

    # Retrieve POSTed form data
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    fname = request.form['fname']
    lname = request.form['lname']

    # Check to see if username already taken. 
    try:
        # If Y, ask for unique username.
        user = User.query.filter(User.username == username).one()
        flash("Already a user. Please pick a unique username or sign in.")

    except:
        # If N taken, add the new user to psql database table Users
        user = User(username=username,
                    password=password,
                    email=email,
                    fname=fname,
                    lname=lname)

        db.session.add(User)
        db.session.commit()

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)