
# ---------------------------------------------------------------------------- #

# Add boolean record to database
    # im = Image.open(boolean_output_image)
    # diff_size_x = im.size[0]
    # diff_size_y = im.size[1]
    # diff_format = im.format
    # diff_mode = im.mode
    # im.close()

    # input_diff_id_1 = session['Image_1_diffID']
    # input_diff_id_2 = session['Image_2_diffID']

    # diff_database_record = db_add_diff_img(user_id,
    #                              input_diff_id_1,
    #                              input_diff_id_2,
    #                              diff_size_x,
    #                              diff_size_y,
    #                              diff_format,
    #                              diff_mode,
    #                              diff_s3_key, #### THIS IS WRONG - currently inherits from InputImage 2
    #                              upload_begin_datetime,
    #                              upload_complete_datetime,
    #                              diff_uuid)

    # session['Boolean_uuid'] = diff_database_record.diff_uuid
    # print(session['Boolean_uuid'])
    # print("Diff added to database with UUID: ", diff_database_record.diff_uuid)


# ---------------------------------------------------------------------------- #

def user_sign_in(submitted_username, submitted_password):
    
    user = UserClass(submitted_username)
    user_record = user.find_by_username()

    # if no existing user
    if user_record and (user_record.password == submitted_password):

        return "Successfully logged in."

    elif user_record:

        return "Username and password do not match."

    else:
        return "Username does not exist. Please register or continue as guest."


#     try:
#         user.find_by_username() # creates self.user_record (row from DB table)
#         user.check_password(request.form['password'])
#         session['username'] = user.username
#         session['user_id'] = user.user_record.user_id # uses self.user_record here

#         flash("Successfully logged in.")

#     except:

#         flash("Login failed. Continue as guest or try again.")



# def user_sign_out():


def current_user():

    user = User.query.filter(User.username == session['username']).one()
    user_id = user.user_id

    return session['username'], user_id

    # username = "tmp"
    # user_id = 1


# ---------------------------------------------------------------------------- #

## DOWNLOAD IMAGE FROM s3
#     try:
        #         s3_dl.Bucket(S3_BUCKET).download_file(image_key, file_location)
            
        #     except botocore.exceptions.ClientError as e:
        #        if e.response['Error']['Code'] == "404":
        #            print("The object does not exist.")
        #        else:
        #            raise
