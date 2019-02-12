"""Flask server for image differencing application"""

from flask import Flask, request, jsonify, render_template, flash, redirect
from model import User, InputImage, DiffImage
from config import *

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/", methods=['POST'])
def diff_imgs_no_login():
    """Diff images without forcing user to sign in"""

    # retrieve images from page
    try:
        img_1 = request.files['img-1']
        img_2 = request.files['img-2']
        flash("Upload success!")
    
    except:
        flash("Please provide two valid files for upload.")
    
    return redirect("/")

    # recognize action when user clicks "diff" button
    # send two images to image diffing function
    # display diff'd image

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