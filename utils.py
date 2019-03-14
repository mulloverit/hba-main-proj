from datetime import datetime
from flask import session

from config import connect_to_db, db, app
from model import User, Project, ChapterBoard, ImageAsset, AssetsToBoardsRelationship, DiffImage

#------------------------------------------------------------------------------#
## CLASS DEFINITIONS ##

### Class establishments ###
# QUESTION:
    # how to handle instance methods that can only be valid
    # once another instance method has been called? ie can't add to db
    # without a valide s3 url -- need an exception?

class ImageClass:

    def __init__(self, image_object, tmp_path, user_id):
        """Instantiate an image object"""

        import uuid
        
        self.user_id = user_id # username
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
            upload_begin_datetime, s3_key, upload_complete_datetime, s3_location
        """
        import boto3, botocore
        from config import s3, s3_dl

        if S3_BUCKET is None:
            return("No S3_BUCKET var set. Check your environment variables!")

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
                            'ContentType': self.mimetype,
                            'ACL': 'public-read',
                            })

            self.upload_complete_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.s3_location = "http://{}.s3.amazonaws.com/{}".format(S3_BUCKET, self.s3_key)

            return "Success"

        except:

            return "Failed"

    def add_to_database(self, user_id, input_image_uuids=None):
        """Create database record for an image. Handles input images & diffs."""

        if input_image_uuids == None:
            
            image_record = ImageAsset(user_id=user_id, 
                    image_size_x=self.size[0],
                    image_size_y=self.size[1],
                    image_format=self.format,
                    image_mode=self.mode,
                    image_s3_url=self.s3_location,
                    image_upload_begin_datetime=self.upload_begin_datetime,
                    image_upload_complete_datetime=self.upload_complete_datetime,
                    image_uuid=self.uuid)

        else:

            input_uuid_1 = input_image_uuids[0]
            input_uuid_2 = input_image_uuids[1]

            input_1_record = ImageAsset.query.filter(ImageAsset.image_uuid == input_uuid_1).first()
            input_2_record = ImageAsset.query.filter(ImageAsset.image_uuid == input_uuid_2).first()

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

class ProjectClass:

    def __init__(self, project_object, user_id):
        """Instantiate an image object"""
        
        self.user_id = user_id # username
        self.project_object = project_object

    def add_to_database(self, user_id):
        """Create database record for an image. Handles input images & diffs."""
        current_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        project_record = Project(user_id=user_id, 
                project_id=self.project_id,
                saved_datetime=current_datetime,
                active="yes")
        
        db.session.add(project_record)
        db.session.commit()

class ChapterBoardClass:

    def __init__(self, chapter_object, user_id):
        """Instantiate an image object"""
        
        self.user_id = user_id # username
        self.chapter_object = chapter_object

    def add_to_database(self, user_id, project_id):
        """Create database record for an image. Handles input images & diffs."""
        
        current_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        chapter_board_record = ChapterBoard(user_id=user_id, 
                project_id=self.project_id,
                saved_datetime=current_datetime,
                active="yes")
        
        db.session.add(chapter_board_record)
        db.session.commit()

class UserClass:
    """Keeps track of metadata about user on site."""

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

    def all_user_items(self):

        all_user_items_list = []
        user = User.query.filter(User.username == self.username).first()
        projects = Project.query.filter(Project.user_id == user.user_id).all()
        chapter_boards = ChapterBoard.query.filter(ChapterBoard.user_id == user.user_id).all()
        image_assets = ImageAsset.query.filter(ImageAsset.user_id == user.user_id).all()
        assets_to_boards = AssetsToBoardsRelationship.query.filter(AssetsToBoardsRelationship.user_id == user.user_id).all()
        
        user_formatted = format_db_results([user])
        projects_formatted = format_db_results(projects)
        chapters_formatted = format_db_results(chapter_boards)
        image_assets_formatted = format_db_results(image_assets)
        assets_to_boards_formatted = format_db_results(assets_to_boards)

        all_user_items_list.extend([user_formatted, projects_formatted, chapters_formatted, image_assets_formatted, assets_to_boards_formatted])

        return all_user_items_list

    def all_image_urls(self):

        all_image_urls = []
        user = User.query.filter(User.username == self.username).first()
        images = ImageAsset.query.filter(ImageAsset.user_id == user.user_id).all()

        for image in images:
            all_image_urls.append(image.image_s3_url)
        
        return(all_image_urls)

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
###############NON CLASS SPECIFIC HELPER FUNCTIONS BELOW HERE###################
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

def format_db_results(query_results, results_as_dict={}, count=0):

    
    all_formatted_results = []
    for result in query_results:
        formatted_results = {}
        formatted_result = str(result).strip('\n').split(":", 1)[1:]
        split_on_line = formatted_result[0].split(",")

        for item in split_on_line:
            key = item.split("=")[0].lstrip().rstrip().strip('\n')
            value = item.split("=")[1].lstrip().rstrip().strip('\n')
            formatted_results[key] = value
        all_formatted_results.append(formatted_results)

    return all_formatted_results


def user_sign_in(submitted_username, submitted_password):
    

    user = UserClass(submitted_username)
    user_record = user.find_by_username()

    if user_record and (user_record.password == submitted_password):
        
        return "Successfully logged in."

    elif user_record:

        return "Username and password do not match."

    else:

        return "Username does not exist. Please register or continue as guest."

def user_sign_out():
    # TO DO
    return "Successfully signed out"

def user_registration_new(submitted_username, submitted_password,
                          submitted_email, submitted_first_name,
                          submitted_last_name):

    user = UserClass(submitted_username, submitted_password,
                     submitted_email, submitted_first_name, submitted_last_name)

    if not user.find_by_username():

        current_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        user_record = User(username=submitted_username, 
                            password=submitted_password,
                            email=submitted_email,
                            fname=submitted_first_name, 
                            lname=submitted_last_name,
                            sign_up_datetime=current_datetime)

        db.session.add(user_record)
        db.session.commit()

        return "Successfully registered. Please sign in."
    
    else:

        return "Already a user. Please pick a unique username or sign in."


def current_user():

    user_record = User.query.filter(User.username == session['username']).one()
    user_id = user_record.user_id

    return session['username'], user_id


# ---------------------------------------------------------------------------- #

## DOWNLOAD IMAGE FROM s3
#     try:
        #         s3_dl.Bucket(S3_BUCKET).download_file(image_key, file_location)
            
        #     except botocore.exceptions.ClientError as e:
        #        if e.response['Error']['Code'] == "404":
        #            print("The object does not exist.")
        #        else:
        #            raise
