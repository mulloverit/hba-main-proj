from datetime import datetime

from config import connect_to_db, db, app
from model import User, InputImage, DiffImage, ImageClass, UserClass 

# ---------------------------------------------------------------------------- #

def user_sign_in(submitted_username, submitted_password):
    

    user = UserClass(submitted_username)
    user_record = user.find_by_username()

    if user_record and (user_record.password == submitted_password):
        
        return "Successfully logged in."

    elif user_record:

        return "Username and password do not match."

    else:

        return "Username does not exist. Please register or continue as guest."


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
