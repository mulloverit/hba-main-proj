"""Flask server for image differencing application"""
from datetime import datetime
from flask import Flask, request, jsonify, render_template, flash, redirect, session
from PIL import Image

from config import *
from s3_manipulation import upload_file_to_s3
from model import User, InputImage, DiffImage

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/", methods=['POST'])
def upload_images():
    """Handle initial image upload [no login required]."""

    # retrieve images from page
    try:
        # img_1, img_2 = request.files['img-1'], request.files['img-2'] # valid?
        img_1 = request.files['img-1']
        img_2 = request.files['img-2']

    except:
        flash("Please provide two valid files for upload.")
        return

    try:
       username = session['username'] 
        
    # IF USER IS LOGGED IN -- upload to user's s3 loc and add to db
    if session.get('username', False):
    
        user = User.query.filter(User.username == session['username']).one()
        user_id = user.user_id
        flash("Logged in.")

        for img in input_imgs:

            # Upload files to S3 
            im = Image.open(img)
            upload_begin_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            im_s3_url = upload_file_to_s3(im.filename, S3_BUCKET, user.username) # from s3_manipulation

            # If valid URL returned, add to db with upload completion time
            if im_s3_url:

                upload_complete_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                success = True
            
            # Otherwise, report a failure with timestamp
            else:
        
                upload_complete_datetime = ("FAILED AT " + datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                success = False

            # Add files to database
            db_add_input_img(username, diff_img, input_1, input_2, succeeded=success) # from database_manipulation

    # IF USER IS NOT LOGGED IN -- upload to tmp s3 loc, do not store in db
    else:

        flash("Not logged in - uploaded images will not persist if page refreshed.")


    flash("Upload success!") # PERHAPS NEEDS TO BE MOVED 
    
    return redirect("/")

# @app.route("/", methods="[POST]")
# def diff_images():
#     """Diff images [no login required]."""

#     # recognize action when user clicks "diff" button
#     # grab records from database and files from s3
#     # send two images to image diffing function --> send to server for diff-ing??
#     # return/render diff'd image



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