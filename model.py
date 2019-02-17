"""Models and database functions for image and user management"""
from config import connect_to_db, db, app

# Used this to clear out previously established table prior to uuid addition
# db.metadata.clear()

### Class establishments ###

class ImageClass:

    def __init__(self, image_object):
        """Instantiate an image object"""

        import uuid
        # self.filepath = filepath
        self.image_object = image_object
        self.uuid = str(uuid.uuid4())
    
        from PIL import Image
        image = Image.open(self.image_object)
        self.size = image.size
        self.format = image.format
        self.mode = image.mode
        self.mimetype = Image.MIME[image.format]
        image.close()



    # def image_metadata(self):
        
    #     from PIL import Image
        
    #     # image = Image.open(self.filepath)
    #     image = Image.open(self.image_object)
    #     image_size = image.size
    #     image_format = image.format
    #     image_mode = image.mode
    #     image_mimetype = Image.MIME[image.format]

    #     image.close()

    #     return {"size": image_size,
    #             "format": image_format,
    #             "mode": image_mode,
    #             "mimetype": image_mimetype}




class User(db.Model):
    """User model."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    sign_up_date = db.Column(db.String(50), nullable=False)

    # TO DO: add class and instance methods to deal with repetitive server tasks
    # # class method takes classmethod decorator
    # @classmethod
    # def find_by_username(username):
    #     """Check if user exists in the database"""

    # # instance methods take self as arg
    # def is_valid_password(self, attempted_password): # model should be agnostic as to where this is coming from, so don't call it "request_password" bc doens't have to be a request --> "attempted_pw"
 
    # # this should maybe be an instance method instead of class method
    # #def check_password_validity(username, user_input_password):
    #     """Check to see if pw matches database record"""

    def __repr__(self):
        """Formatted output when class obj is returned. Does not return email or password."""
        return(f"""<User:
                        user_id={self.user_id},
                        username={self.username}),
                        sign_up_date={self.sign_up_date}""")


class InputImage(db.Model):
    """Input image model."""

    __tablename__ = "input_images"

    im_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    im_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    im_upload_begin_datetime = db.Column(db.String(50), nullable=False)
    im_upload_complete_datetime = db.Column(db.String(50), nullable=False)
    im_size_x = db.Column(db.Integer, nullable=False)
    im_size_y = db.Column(db.Integer, nullable=False)
    im_format = db.Column(db.String(10), nullable=False)
    im_mode = db.Column(db.String(10), nullable=False)
    im_s3_url = db.Column(db.String(1000), nullable=False)
    im_uuid = db.Column(db.String(500), nullable=False)


    def __repr__(self):
        """Formatted output when class obj is returned. Does not return password."""
        return (f"""<InputImage:
                    im_id={self.im_id}, 
                    im_user_id={self.im_user_id}), 
                    im_upload_begin_datetime={self.im_upload_begin_datetime},
                    im_upload_complete_datetime={self.im_upload_complete_datetime},
                    im_size_x={self.im_size_x},
                    im_size_y={self.im_size_y},
                    im_format={self.im_format},
                    im_mode={self.im_mode},
                    im_s3_url={self.im_s3_url},
                    im_uuid={self.im_uuid}""")


class DiffImage(db.Model):
    """Input image model."""

    __tablename__ = "diff_images"

    diff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diff_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    im_1_id = db.Column(db.Integer, db.ForeignKey('input_images.im_id'))
    im_2_id = db.Column(db.Integer, db.ForeignKey('input_images.im_id'))
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