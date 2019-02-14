"""Utility file for interacting with main database"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
import os
from PIL import Image
from sqlalchemy import func

from config import db
from model import User, InputImage, DiffImage

CURRENT_DATE = datetime.today().strftime('%m-%d-%Y')

def db_check_if_user_exists(username):
    return User.query.filter(User.username == username).one()

def db_add_new_user(username, email, password, fname, lname):
    """Load new user from into db"""

    # user_id not included, as it should populate automatically
    user = User(username=username,
                email=email,
                password=password,
                fname=fname,
                lname=lname,
                sign_up_date=CURRENT_DATE)

    db.session.add(user)
    db.session.commit()

def db_add_input_img(user_id, upload_begin_datetime, upload_complete_datetime):
    """Load input img data into db"""
    
    im = Image.open(img)

    input_image = InputImage(im_user_id=user_id, 
            im_upload_begin_datetime=upload_begin_datetime,
            im_upload_complete_datetime=upload_complete_datetime,
            im_size_x=im.size[0],
            im_size_y=im.size[1],
            im_format=im.format,
            im_mode=im.mode,
            im_s3_url=im_s3_url)

    db.sesssion.add(input_image)
    db.session.commit()
    im.close()

def db_add_diff_img(user_id, input_1, input_2, upload_begin_datetime,
                     upload_complete_datetime):
    """Load fake diff img data from test-fixtures/diff-imgs.txt"""

    # NEEDS LOGIC FOR GETTING IMAGE METADATA

    diff_img = DiffImage(diff_user_id=diff_user_id,
                         im_1_id=im_1_id,
                         im_2_id=im_2_id,
                         diff_size_x=diff_size_x,
                         diff_size_y=diff_size_y,
                         diff_format=diff_format,
                         diff_mode=diff_mode,
                         diff_s3_url=diff_s3_url,
                         diff_upload_date=CURRENT_DATE)
    
    db.session.add(diff_img)
    db.session.commit()