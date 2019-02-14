"""Flask server for image differencing application"""
from datetime import datetime
from flask import Flask, request, jsonify, render_template, flash, redirect, session
from PIL import Image
from werkzeug.utils import secure_filename

from config import *
from database_manipulation import *
from model import User, InputImage, DiffImage
from s3_manipulation import upload_file_to_s3

app.secret_key = "what"
TMP_UPLOAD_FOLDER = "tmp/uploads/"
ALLOWED_FORMATS = set(['png', 'jpg', 'jpeg', 'tif'])
app.config['TMP_UPLOAD_FOLDER'] = TMP_UPLOAD_FOLDER

def allowed_file_formats(filename):
    """Utility for checking uploaded image formats"""

    # Returns boolean (T/F) based on whether file ext exists AND is in allowed formats set
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_FORMATS

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
def upload_input_images():
    """Handle initial image upload [no login required]."""

    # retrieve images from page
    try:
        input_imgs = [request.files['img-1'], request.files['img-2']]
        flash("Upload success!") # PERHAPS NEEDS TO BE MOVED 

    except:
        flash("Please provide two valid files for upload.")
        return redirect("/")

    # If a user is logged in, add their uploads to database and s3
    try:
        username = session['username']
        user = User.query.filter(User.username == session['username']).one()
        user_id = user.user_id

        for img in input_imgs:

            upload_begin_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            im_s3_url = upload_file_to_s3(img, S3_BUCKET, user.username) # WORKING? PROB NOT
        
            if im_s3_url: # If valid URL returned, add to db with upload completion time
                upload_complete_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
            else: # Otherwise, record a failure with timestamp and notify user
                upload_complete_datetime = ("FAILED AT " + datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                flash("Logging file to S3 failed.")

            # Add record to database
            db_add_input_img(img,
                             user_id,
                             input_1,
                             input_2,
                             upload_begin_datetime,
                             upload_complete_datetime) 

    # If user not logged in, don't do any more work.
    except:

        flash("Not logged in - images temporarily saved.")

        for img in input_imgs:
            if allowed_file_formats(img.filename):
                imgname = secure_filename(img.filename)
                img.save(os.path.join(app.config['TMP_UPLOAD_FOLDER'], imgname))

        flash("Click `Diff` button for result!")
    
    return redirect("/")

@app.route("/submit-diff-request", methods=['POST'])
def diff_images():
    """Diff images [no login required]."""

    # grab images from tmp folder
    diff_img = create_boolean_diff(input_imgs[0], input_imgs[1])
    diff_img.show()

    return redirect("/")
    
@app.route("/upload-diff", methods=['POST'])
def upload_diff():
    """Upload diff to s3 for users who are logged in"""
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)