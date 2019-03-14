"""Utility file to seed image_diffs database for testing"""
from datetime import datetime
import os
from sqlalchemy import func

from config import connect_to_db
from model import User, ImageAsset, DiffImage, Project, ChapterBoard, db
from server import app

CURRENT_DATETIME = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

def load_users():
    """Load fake users from test-fixtures/users.txt"""

    print("Users")

    # empty user table if any records exist
    # User.query.delete()

    for row in open("test-fixtures/users.txt"):
        row = row.rstrip()
        username, email, password, fname, lname = row.split("|")

        # user_id not included, as it should populate automatically
        user = User(username=username,
                    email=email,
                    password=password,
                    fname=fname,
                    lname=lname,
                    sign_up_datetime=CURRENT_DATETIME)

        db.session.add(user)
    db.session.commit()

def load_projects():
    """Load fake input img data from test-fixtures/input-imgs.txt"""
    print("Projects")

    # clean out any existing records from table
    # Project.query.delete()

    for row in open("test-fixtures/projects.txt"):
        row = row.rstrip()
        user_id, project_name, project_description, active = row.split("|")

        project = Project(user_id=user_id,
                          project_name=project_name,
                          project_description=project_description,
                          active=active)

        db.session.add(project)
    db.session.commit()


def load_chapter_boards():

    print("Chapter boards")
    # ChapterBoard.query.delete()

    for row in open("test-fixtures/chapter_boards.txt"):
        
        row = row.rstrip()
        user_id, project_id, active = row.split("|")
        
        chapter_board = ChapterBoard(user_id=user_id, 
                                     project_id=project_id,
                                     active=active)

        db.session.add(chapter_board)
    db.session.commit()



def load_image_assets():
    """Load fake input img data from test-fixtures/input-imgs.txt"""
    print("Image assets")

    # clean out any existing records from table
    # ImageAsset.query.delete()

    for row in open("test-fixtures/image_assets.txt"):
        row = row.rstrip()
        im_user_id, im_size_x, im_size_y, im_format, im_mode, im_s3_url, img_uuid = row.split("|")

        input_img = ImageAsset(user_id=im_user_id,
                               image_size_x=im_size_x,
                               image_size_y=im_size_y,
                               image_format=im_format,
                               image_mode=im_mode,
                               image_s3_url=im_s3_url,
                               image_upload_begin_datetime=CURRENT_DATETIME,
                               image_upload_complete_datetime=CURRENT_DATETIME,
                               image_uuid=img_uuid)

        db.session.add(input_img)
    db.session.commit()

def load_diff_images():
    """Load fake diff img data from test-fixtures/diff-imgs.txt"""
    print("Diff images")

    # clean out any existing records from table
    # DiffImage.query.delete()

    for row in open("test-fixtures/diff-images.txt"):
        row = row.rstrip()
        diff_user_id, im_1_id, im_2_id, diff_size_x, diff_size_y, diff_format, diff_mode, diff_s3_url, img_uuid = row.split("|")

        diff_img = DiffImage(diff_user_id=diff_user_id,
                             im_1_id=im_1_id,
                             im_2_id=im_2_id,
                             diff_size_x=diff_size_x,
                             diff_size_y=diff_size_y,
                             diff_format=diff_format,
                             diff_mode=diff_mode,
                             diff_s3_url=diff_s3_url,
                             diff_upload_begin_datetime=CURRENT_DATETIME,
                             diff_upload_complete_datetime=CURRENT_DATETIME,
                             diff_uuid=img_uuid)

        db.session.add(diff_img)
    db.session.commit()

if __name__ == "__main__":

    # creates tables, in case they haven't been created yet
    os.system("dropdb storybored")
    os.system("createdb storybored")
    connect_to_db(app)
    db.create_all()
    db.session.commit()

    load_users()
    load_image_assets()
    load_projects()
    load_chapter_boards()
    # # load_diff_images()
