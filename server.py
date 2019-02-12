"""Flask server for image differencing application"""

from flask import Flask, request, jsonify, render_template
from model import User, InputImage, DiffImage
from config import *


app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/")
def show_index():
        """Index/homepage"""

        return render_template("index.html")

@app.route("/signin", methods=['POST'])
def sign_in():
    """Add user to database"""

    username = request.form['username']
    password = request.form['password']

    try:
        user = User.query.filter(User.username == username).one()

        if user.password == password:

            session['username'] = username
            flash("Successfully logged in")

            return render_template("index.html")

    except:
        return redirect("/register")

@app.route("/register-new", methods=['POST'])
def register_user():
    """Add user to database"""

    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    fname = request.form['fname']
    lname = request.form['lname']

    try:
        user = User.query.filter(User.username == username).one()
        flash("Already a user. Please pick a unique username or sign in.")

    except:
        user = User(username=username,
                    password=password,
                    email=email,
                    fname=fname,
                    lname=lname)

        db.session.add(User)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)