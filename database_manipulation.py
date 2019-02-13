"""Utility file for interacting with main database"""
from datetime import datetime
import os
from PIL import Image
from sqlalchemy import func

from model import User, InputImage, DiffImage, connect_to_db, db
from s3_manipulation import upload_file_to_s3


CURRENT_DATE = datetime.today().strftime('%m-%d-%Y')

def db_add_new_users(username, email, password??, fname, lname):
    """Load new user from into db"""

    # NEEDS LOGIC TO PARSE USER DATA ! WHAT TO DO WITH PW?

    # user_id not included, as it should populate automatically
    user = User(username=username,
                email=email,
                password=password,
                fname=fname,
                lname=lname,
                sign_up_date=CURRENT_DATE)

    db.session.add(user)

    db.session.commit()

def db_add_input_img(username, diff_img, input_1, input_2, succeeded=True):
    """Load input img data into db"""
    
    im = Image.open(img)
    upload_begin_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    
    if succeeded:
        im_s3_url = upload_file_to_s3(im.filename, S3_BUCKET, user.username)
        upload_complete_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    else:
        # will require database to handle date/datetime as a string instead of datetime obejct
        upload_complete_datetime = ("FAILED AT " + datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

    input_image = InputImage(im_user_id=user_id, 
            im_upload_begin_datetime=upload_begin_current_datetime,
            im_upload_complete_datetime=upload_complete_current_datetime,
            im_size_x=im.size[0],
            im_size_y=im.size[1],
            im_format=im.format,
            im_mode=im.mode,
            im_s3_url=im_s3_url)

    im.close()
    db.sesssion.add(input_image)
    db.session.commit()

def db_add_diff_img(username, diff_img, input_1, input_2):
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

if __name__ == "__main__":

    connect_to_db(app)