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
from diff_logic import *
from model import User, InputImage, DiffImage, ImageClass, UserClass
from utils import *


app.secret_key = "what"


@app.route("/")
def show_index():
    """Index/homepage"""

    session['username'] = 'tmp'
    return render_template("index.html")


@app.route("/sign-in", methods=['POST'])
def sign_in():
    """Log in an existing user"""
    print("OK 1")
    print(request.form)
    message = user_sign_in(request.form['username'], request.form['password'])

    if "Success" in message:
        session['username'] = request.form['username']

    username = request.form['username']
    print(username)
    flash (message)

    return render_template("main.html", username=username)


@app.route("/register-new", methods=['POST'])
def register_user():
    """Add a new user to database"""

    message = user_registration_new(request.form['username'], request.form['password'],
                     request.form['email'], request.form['fname'], request.form['lname'])
    
    flash (message)

    return render_template("main.html")


@app.route("/upload-inputs", methods=['POST'])
def upload_inputs():
    """Handle initial image upload [no login required]."""

    username, user_id = current_user()

    try:
        
        user_submitted_image_s3_locations = []
        # session['request_image_uuids'] = []

        for user_submitted_image in [request.files['img-1'], request.files['img-2']]:
            
            user_submitted_image_temporary_path = ('static/images/{}_{}'.format(
                                                username,
                                                user_submitted_image.filename))
            
            user_submitted_image.save(user_submitted_image_temporary_path)
            
            user_submitted_image_object = ImageClass(user_submitted_image,
                                            user_submitted_image_temporary_path,
                                            username,
                                            )
            
            user_submitted_image_object.upload_to_s3(S3_BUCKET)
            
            user_submitted_image_object.add_to_database(user_id)
            
            user_submitted_image_s3_locations.append(
                                            user_submitted_image_object.s3_location,
                                            )
            
            # session['request_image_uuids'].append(
            #                     user_submitted_image_object.uuid,
            #                     )
            
            print(user_submitted_image_object.s3_location)
        
        flash("Upload to S3 a success!")

        # return render_template("index.html",
        #             image_1=session['user_submitted_image_temporary_paths'][0],
        #             image_2=session['user_submitted_image_temporary_paths'][1],
        #             )


        # return jsonify(image_1=session['user_submitted_image_temporary_paths'][0],
        #                image_2=session['user_submitted_image_temporary_paths'][1],
        #                )

        # images = jsonify(image_locations=user_submitted_image_s3_locations)
        
        # return render_template("index.html", images=images)
        return render_template("main.html", images=user_submitted_image_s3_locations)
        # return jsonify(session['user_submitted_image_temporary_paths'])
        # OR TRY TO JSONIFY THIS and return just json instead of a render_template    !!
        # return      (image_1=session['user_submitted_image_temporary_paths'][0],
        #             image_2=session['user_submitted_image_temporary_paths'][1],
        #             )

    except:

        flash("Please provide two valid files for upload.")
        # return render_template("index.html")
        return jsonify("hi - your upload failed")


@app.route("/submit-diff-request", methods=['POST'])
def diff_images():
    """Diff images from local dir [no s3 and no login required]."""
    
    username, user_id = current_user()

    try:

        boolean_diff_path = create_boolean_diff(
                                session['user_submitted_image_temporary_paths'][0],
                                session['user_submitted_image_temporary_paths'][1],
                                )
        
        difference_image = ImageClass(boolean_diff_path, boolean_diff_path,
                                      username) # wants path not PIL object as 1st arg

        difference_image.upload_to_s3(S3_BUCKET)
        
        difference_image.add_to_database(user_id,
                                input_image_uuids=session['request_image_uuids'])

        flash("Diff succeeded.")

    except:

        flash("Diff failed :(")

    return render_template("main.html",
                    image_1=session['user_submitted_image_temporary_paths'][0],
                    image_2=session['user_submitted_image_temporary_paths'][1],
                    difference_image=boolean_diff_path)
    

if __name__ == "__main__":
    app.run(debug=True)