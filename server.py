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
        
    # IF USER IS LOGGED IN -- add to database and upload to s3
    if session.get('username', False):
    
        user = User.query.filter(User.username == session['username']).one()
        user_id = user.user_id

        for img in input_imgs:

            current_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            im = Image.open(img)

            im_s3_url = upload_file_to_s3(im.filename, S3_BUCKET, user.username)

            input_image = InputImage(im_user_id=user_id, 
                    im_upload_datetime=current_datetime,
                    im_size_x=im.size[0],
                    im_size_y=im.size[1],
                    im_format=im.format,
                    im_mode=im.mode,
                    im_s3_url=im_s3_url)

            db.sesssion.add(input_image)
        db.session.commit()
        flash("Logged in. Files will persist after page refresh.")

    else:
        flash("Not logged in - uploaded images will not persist if page refreshed.")

        # If user is logged in and we don't neeed to add to database,
        # let them know we've recieved temp images

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