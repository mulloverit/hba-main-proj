"""Flask server for image differencing application"""
from io import StringIO, BytesIO
from datetime import datetime
from flask import Flask, request, json, jsonify, make_response, render_template, flash, redirect, session
import os
from PIL import Image
import uuid
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage

from config import *
from utils import *

app.secret_key = "what"

@app.route("/")
def show_index():
    """Index/homepage"""

    return render_template("index.html")

@app.route("/get-started", methods=['POST'])
def get_started():
    """Sign-in and registration page"""

    return render_template("get-started.html")


@app.route("/guest-continue", methods=['POST'])
def guest_continue():
    
    session['username'] = 'guest'

    return redirect('/main')

@app.route("/sign-in", methods=['POST'])
def sign_in():
    """Log in an existing user"""
    
    message = user_sign_in(request.form['username'], request.form['password'])

    if "Success" in message:
        session['username'] = request.form['username']


    return redirect('/main')

@app.route("/sign-out", methods=['POST'])
def sign_out():
    """Log in an existing user"""

    session['username'] = "guest"
    message = user_sign_out()
    return redirect('/')


@app.route("/register-new", methods=['POST'])
def register_user():
    """Add a new user to database"""

    message = user_registration_new(request.form['username'], request.form['password'],
                     request.form['email'], request.form['fname'], request.form['lname'])
    
    flash (message)

    return redirect('/main')


@app.route("/upload-inputs", methods=['POST'])
def upload_inputs():
    """Handle initial image upload [no login required]."""

    username, user_id = current_user()
    user = UserClass(username)
    user_submitted_image_s3_locations = []
    
    try:
    
        for file in request.files:
            
            user_submitted_image = request.files.get(file)
            
            user_submitted_image_temporary_path = ('static/images/{}_{}'.format(
                                                username,
                                                user_submitted_image.filename))

            user_submitted_image.save(user_submitted_image_temporary_path)
        
            user_submitted_image_object = ImageClass(user_submitted_image,
                                            user_submitted_image_temporary_path,
                                            username,
                                            )
            
            print(user_submitted_image_object.upload_to_s3(S3_BUCKET))

            user_submitted_image_object.add_to_database(user_id)
            
            user_submitted_image_s3_locations.append(
                                            user_submitted_image_object.s3_location,
                                            )    
            
        images = user.all_image_urls()

        print("UPLOAD SUCCESS!")
        print("NEW ASSET LOCATIONS:", user_submitted_image_s3_locations)
        print("ALL USER IMAGES:", images)
        
        #normalize data to a dictionary and Json.dumps similar to boards below
        return str(images)

    except:


        return jsonify("hi - your upload failed")

@app.route("/save-as", methods=['POST'])
def save_as():

    jayson = json.loads(request.form.get('userChapterBoards'))

    for item in jayson:
        # print("JSON ITEM", item)
        print(item.get('boardAssets'))
    
    return "hello"

@app.route("/main")
def main():

    username, user_id = current_user()
    user = UserClass(username)
    images = user.all_image_urls()
    all_user_items = user.all_user_items()

    user_record = all_user_items[0]
    projects_records = all_user_items[1]
    chapter_board_records = all_user_items[2]
    image_asset_records = all_user_items[3]
    assets_to_boards_rel = all_user_items[4]

    chapters = {}
    active_boards_by_id = set()

    for item in chapter_board_records:
        print("chapter board", item)
        if item['active'] == 'yes':
            active_boards_by_id.add(item['board_id'])

    board_with_assets = {}
    # for a given board id
    for board in active_boards_by_id:
        # go through all board rels
        for item in assets_to_boards_rel:
            # if board id matches a bord rel record
            if item['board_id'] == board:
                # give me the asset id of that item so i can get the url later
                if board_with_assets.get(board, None):
                    board_with_assets[board].append(item['asset_id'])
                else:
                    board_with_assets[board] = [item['asset_id']]

    board_with_urls = {}
    for board, assets in board_with_assets.items():
        asset_urls = []
        for asset in assets:
            for asset_record in image_asset_records:
                if asset_record['image_id'] == asset:
                    asset_urls.append(asset_record['image_s3_url'])

        board_with_urls[board] = asset_urls

    chapter_boards_with_asset_urls = {}
    count = 0 
    for board, asset_urls in board_with_urls.items():
        chapter_boards_with_asset_urls[count] = {"boardName": board,
                                                 "boardAssets": asset_urls}
        count += 1
    print("formatted", chapter_boards_with_asset_urls)

    chapters = chapter_boards_with_asset_urls
    # chapters = {"boardName": "board_00001", "boardAssets": ['http://hackbright-image-upload-test.s3.amazonaws.com/guest/c55db769-59a9-470e-9678-0768c7b0d73e_static/images/guest_DODtrQ5W0AA-2S4.jpg', 'http://hackbright-image-upload-test.s3.amazonaws.com/guest/346b5e60-9dcc-43ec-9657-001cd0dbb49c_static/images/guest_IMG_5417.JPG']}, {"boardName": "board_00002", "boardAssets": ['http://hackbright-image-upload-test.s3.amazonaws.com/guest/346b5e60-9dcc-43ec-9657-001cd0dbb49c_static/images/guest_IMG_5417.JPG', 'http://hackbright-image-upload-test.s3.amazonaws.com/guest/c7f56f81-8ebc-4533-8bd3-d0b605db2595_static/images/guest_IMG_5477.JPG', 'http://hackbright-image-upload-test.s3.amazonaws.com/guest/9d85f98c-f07b-4d6a-9b3c-cb7b697f4a13_static/images/guest_DODtrQ5W0AA-2S4.jpg', 'http://hackbright-image-upload-test.s3.amazonaws.com/guest/40b0e5bb-4bbc-4dae-85e6-436b8a6f64ee_static/images/guest_IMG_5417.JPG']}
    chapters = json.dumps(chapters)
    chapters = json.loads(chapters)

    return render_template("main.html",
                            username=username,
                            images=images,
                            chapters=chapters)

if __name__ == "__main__":
    app.run(debug=True)