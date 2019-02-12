"""Utility file to seed image_diffs database for testing"""

from sqlalchemy import func
from model import User, InputImage, DiffImage
from datetime import datetime

from model import connect_to_db, db
from server import app

CURRENT_DATE = datetime.today().strftime('%m-%d-%Y')

def load_users():
    """Load fake users from test-fixtures/users.txt"""

    print("Users")

    # empty user table if any records exist
    User.query.delete()

    for row in open("test-fixtures/users.txt"):
        row = row.rstrip()
        username, email, password, fname, lname = row.split("|")

        # user_id not included, as it should populate automatically
        user = User(username=username,
                    email=email,
                    password=password,
                    fname=fname,
                    lname=lname,
                    sign_up_date=CURRENT_DATE)

        db.session.add(user)

    db.session.commit()

def load_input_imgs():
    """Load fake input img data from test-fixtures/input-imgs.txt"""
    print("Input images")

    # clean out any existing records from table
    InputImage.query.delete()

    for row in open("test-fixtures/input-images.txt"):
        row = row.rstrip()
        im_user_id, im_size_x, im_size_y, im_format, im_mode, im_s3_url = row.split("|")

        input_img = InputImage(im_user_id=im_user_id,
                               im_size_x=im_size_x,
                               im_size_y=im_size_y,
                               im_format=im_format,
                               im_mode=im_mode,
                               im_s3_url=im_s3_url,
                               im_upload_date=CURRENT_DATE)

        db.session.add(input_img)

    db.session.commit()

def load_diff_imgs():
    """Load fake diff img data from test-fixtures/diff-imgs.txt"""
    print("Diff images")

    # clean out any existing records from table
    DiffImage.query.delete()

    for row in open("test-fixtures/input-images.txt"):
        row = row.rstrip()
        (diff_user_id, im_1_id, im_2_id, diff_size_x, diff_size_y, 
            diff_format, diff_mode, diff_s3_url = row.split("|")) 

        diff_img = DiffImage(diff_user_id=diff_user_id,
                             im_1_id=im_1_id,
                             im_2_id=im_2_id,
                             diff_size_x=diff_size_x,
                             diff_size_y=diff_size_y,
                             diff_format=diff_format,
                             diff_mode=diff_mode,
                             diff_s3_url=diff_s3_url,
                             diff_upload_date=CURRENT_DATE)

if __name__ == "__main__":

    # creates tables, in case they haven't been created yet
    connect_to_db(app)
    db.create_all()

    load_users()
    # load_input_imgs()
    # load_diff_imgs()
