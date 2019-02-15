"""Utility file for interacting with main database"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from PIL import Image
from sqlalchemy import func

from config import db
from model import User, InputImage, DiffImage



def db_check_if_user_exists(username):
    return User.query.filter(User.username == username).one()

def db_add_new_user(username, email, password, fname, lname):
    """Load new user from into db"""

    current_date = datetime.today().strftime('%m-%d-%Y')
    
    # user_id not included, as it should populate automatically
    user = User(username=username,
                email=email,
                password=password,
                fname=fname,
                lname=lname,
                sign_up_date=current_date)

    db.session.add(user)
    db.session.commit()

def db_add_input_img(user_id, img_size_x, img_size_y, img_format,
                     img_mode, img_s3_url, upload_begin_datetime,
                     upload_complete_datetime, img_uuid):
    """Load input img data into db"""

    input_image = InputImage(user_id=user_id, 
            im_size_x=img_size_x,
            im_size_y=img_size_y,
            im_format=img_format,
            im_mode=img_mode,
            im_s3_url=img_s3_url,
            im_upload_begin_datetime=upload_begin_datetime,
            im_upload_complete_datetime=upload_complete_datetime,
            im_uuid=uuid)

    # need a way to return image_id to server.py
    db.sesssion.add(input_image)
    db.session.commit()
    return("success")

def db_add_diff_img(img, user_id, im_1_id, im_2_id, diff_s3_url, upload_begin_datetime,
                     upload_complete_datetime, uuid):
    """Load fake diff img data from test-fixtures/diff-imgs.txt"""

    # NEEDS LOGIC FOR GETTING IMAGE METADATA
    diff = Image.open(img)

    diff_img = DiffImage(diff_user_id=user_id,
                         im_1_id=im_1_id,
                         im_2_id=im_2_id,
                         diff_size_x=diff.size[0],
                         diff_size_y=diff.size[1],
                         diff_format=diff.format,
                         diff_mode=diff.mode,
                         diff_s3_url=diff_s3_url,
                         diff_upload_begin_datetime=upload_begin_datetime,
                         diff_upload_complete_datetime=upload_complete_datetime,
                         diff_uuid=uuid)
    
    db.session.add(diff_img)
    db.session.commit()