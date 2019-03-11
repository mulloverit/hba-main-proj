"""Models and database functions for image and user management"""
from config import connect_to_db, db, app
from datetime import datetime

# Used this to clear out previously established table prior to uuid addition
# db.metadata.clear()

class User(db.Model):
    """User model."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    sign_up_datetime = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Formatted output when class obj is returned. Does not return email or password."""

        return(f"""<User:
                        user_id={self.user_id},
                        username={self.username},
                        sign_up_datetime={self.sign_up_datetime}""")


class InputImage(db.Model):
    """Input image model."""

    __tablename__ = "input_images"

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    image_upload_begin_datetime = db.Column(db.String(50), nullable=False)
    image_upload_complete_datetime = db.Column(db.String(50), nullable=False)
    image_size_x = db.Column(db.Integer, nullable=False)
    image_size_y = db.Column(db.Integer, nullable=False)
    image_format = db.Column(db.String(10), nullable=False)
    image_mode = db.Column(db.String(10), nullable=False)
    image_s3_url = db.Column(db.String(1000), nullable=False)
    image_uuid = db.Column(db.String(500), nullable=False)


    def __repr__(self):
        """Formatted output when class obj is returned. Does not return password."""

        return (f"""<InputImage:
                    image_id={self.image_id}, 
                    image_user_id={self.image_user_id}), 
                    image_upload_begin_datetime={self.image_upload_begin_datetime},
                    image_upload_complete_datetime={self.image_upload_complete_datetime},
                    image_size_x={self.image_size_x},
                    image_size_y={self.image_size_y},
                    image_format={self.image_format},
                    image_mode={self.image_mode},
                    image_s3_url={self.image_s3_url},
                    image_uuid={self.image_uuid}""")


class ChapterBoard(db.Model):
    """User saved asset groups"""

    __tablename__ = "chapter_boards"

    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    board_uuid = db.Column(db.String(500), nullable=False)
    board_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    board_asset_list = db.Column(db.String,nullable=False)
    saved_datetime = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Formatted output when chapter board is returned"""

        return (f"""<ChapterBoard:
                    board_id={self.board_id},
                    board_uuid={self.board_uuid},
                    board_user_id={self.board_user_id},
                    board_asset_list={self.board_asset_list},
                    saved_datetime={self.saved_datetime}""")


class DiffImage(db.Model):
    """Input image model."""

    __tablename__ = "diff_images"

    diff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diff_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    im_1_id = db.Column(db.Integer, db.ForeignKey('input_images.image_id'))
    im_2_id = db.Column(db.Integer, db.ForeignKey('input_images.image_id'))
    diff_upload_begin_datetime = db.Column(db.String(50), nullable=False)
    diff_upload_complete_datetime = db.Column(db.String(50), nullable=False)
    diff_size_x = db.Column(db.Integer, nullable=False)
    diff_size_y = db.Column(db.Integer, nullable=False)
    diff_format = db.Column(db.String(10), nullable=False)
    diff_mode = db.Column(db.String(10), nullable=False)
    diff_s3_url = db.Column(db.String(500), nullable=False)
    diff_uuid = db.Column(db.String(500), nullable=False)


    def __repr__(self):
        """Formatted output when class obj is returned. Does not return password."""

        return (f"""<DiffImage:
                    diff_id={self.diff_id}, 
                    diff_user_id={self.diff_user_id}),
                    im_1_id={self.im_1_id},
                    im_2_id={self.im_2_id},
                    diff_upload_begin_datetime={self.diff_upload_begin_datetime},
                    diff_upload_complete_datetime={self.diff_upload_complete_datetime},
                    diff_size_x={self.diff_size_x},
                    diff_size_y={self.diff_size_y},
                    diff_format={self.diff_format},
                    diff_mode={self.diff_mode},
                    diff_s3_url={self.diff_s3_url},
                    diff_uuid={self.diff_uuid}""")

# if __name__ == "__main__":
#     from server import app
#     connect_to_db(app)
#     print("Connected to DB.")