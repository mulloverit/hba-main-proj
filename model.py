"""Models and database functions for image and user management"""
from config import connect_to_db, db, app
from datetime import datetime

# Used this to clear out previously established table prior to uuid addition
# db.metadata.clear()

### Class establishments ###

class ImageClass:

    # QUESTION:
    # how to handle instance methods that can only be valid
    # once another instance method has been called? ie can't add to db
    # without a valide s3 url -- need an exception?

    def __init__(self, image_object, tmp_path, owner):
        """Instantiate an image object"""

        import uuid
        
        self.owner = owner # username
        self.tmp_path = tmp_path
        self.image_object = image_object
        self.uuid = str(uuid.uuid4())
    
        from PIL import Image

        image = Image.open(self.image_object)
        self.size = image.size
        self.format = image.format
        self.mode = image.mode
        self.mimetype = Image.MIME[image.format]
        #image.close()

    def upload_to_s3(self, S3_BUCKET):
        """ Uploads an image file to s3, creating instance attributes:
            - upload_begin_datetime
            - s3_key
            - upload_complete_datetime
            - s3_location
        """

        import boto3, botocore
        from config import s3, s3_dl
        #from datetime import datetime

        try:

            self.upload_begin_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.s3_key = self.owner + "/" + self.uuid + "_" + self.tmp_path
            
            # Halleluja, get past "ValueError: Fileobj must implement read"
            # https://www.programcreek.com/python/example/106649/boto3.s3.transfer.ProgressCallbackInvoker
            with open(self.tmp_path, 'rb') as data:
                s3.upload_fileobj(
                        data,
                        S3_BUCKET,
                        self.s3_key,
                        ExtraArgs={
                            'ContentType': self.mimetype
                            })

            self.upload_complete_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.s3_location = "http://{}.s3.amazonaws.com/{}".format(S3_BUCKET, self.s3_key)

            return "Success"

        except:

            return "Failed"

    # def get_id_by_uuid(self):

    #     InputImage.query.filter(InputImage.image_uuid == input_uuid_1).first()

    def add_to_database(self, user_id, input_images=None):
        """Create database record for an image. Handles input images & diffs."""


        if input_images == None:

            image_record = InputImage(image_user_id=user_id, 
                    image_size_x=self.size[0],
                    image_size_y=self.size[1],
                    image_format=self.format,
                    image_mode=self.mode,
                    image_s3_url=self.s3_location,
                    image_upload_begin_datetime=self.upload_begin_datetime,
                    image_upload_complete_datetime=self.upload_complete_datetime,
                    image_uuid=self.uuid)

        else:

            input_uuid_1 = input_images[0]
            input_uuid_2 = input_images[1]

            input_1_record = InputImage.query.filter(InputImage.image_uuid == input_uuid_1).first()
            input_2_record = InputImage.query.filter(InputImage.image_uuid == input_uuid_2).first()
            
            image_record = DiffImage(diff_user_id=user_id,
                                 im_1_id=input_1_record.image_id,
                                 im_2_id=input_2_record.image_id,
                                 diff_size_x=self.size[0],
                                 diff_size_y=self.size[1],
                                 diff_format=self.format,
                                 diff_mode=self.mode,
                                 diff_s3_url=self.s3_location,
                                 diff_upload_begin_datetime=self.upload_begin_datetime,
                                 diff_upload_complete_datetime=self.upload_complete_datetime,
                                 diff_uuid=self.uuid)

        db.session.add(image_record)
        db.session.commit()

class UserClass:

    def __init__(self, username, password=None, email=None,
                 first_name=None, last_name=None):

                 self.username = username
                 self.password = password
                 self.email = email
                 self.first_name = first_name
                 self.last_name = last_name

    def find_by_username(self):
        """Search for a user record in database based on username. If user 
            does not exist, return None."""
        try:

            self.user_record = User.query.filter(User.username == self.username).first()
            return self.user_record
    
        except:

            return None

    # # this should really be a "sign-in" utility
    # def check_password(self, submitted_password):
    #     """Check a user submitted password against database record password
    #         for specified username. If they do not match, return None."""
    #     try:

    #         self.user_record.password == submitted_password

    #     except:

    #         return None

    def register_new(self):
        """Register a new user, add them to the database."""

        current_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        user_record = User(username=self.username, 
                            email=self.email, 
                            password=self.password,
                            fname=self.first_name, 
                            lname=self.last_name,
                            sign_up_datetime=current_datetime)

        db.session.add(user_record)
        db.session.commit()


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