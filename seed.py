"""Utility file to seed image_diffs database for testing"""

from sqlalchemy import func
from model import User, InputImage, DiffImage
from datetime import datetime

from model import connect_to_db, db
from server import app

def load_users():
    """Load fake userse from test-fixtures/users.txt"""

    print("Users")

    # empty user table if any records exist
    User.query.delete()

    for row in open("test-fixtures/users.txt"):
        row = row.rstrip()
        username, email, password, fname, lname = row.split("|")

        # user_id and date not included, as they should populate automatically
        user = User(username=username,
                    email=email,
                    password=password,
                    fname=fname,
                    lname=lname)

        db.session.add(user)

    db.session.commit()


if __name__ == "__main__":

    # creates tables, in case they haven't been created yet
    db.create_all()

    load_users()
    # load_input_imgs()
    # load_diff_imgs()
