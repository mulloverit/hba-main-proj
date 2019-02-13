"""Utility file for interacting with AWS S3"""
import boto3, botocore
from PIL import Image, ImageChops, ImageStat # imagechops -> "image channel operations"

def upload_file_to_s3(file, bucket_name, username, acl="private"):
    """Upload a file to S3 location specific to a user"""
    try:
        
        bucket_loc = bucket_name + "/" + username

        s3.upload_fileobj(
            file,
            bucket_loc,
            file.filename, # what is .filename ?
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            })

        return "{}{}".format(app.config["S3_LOCATION"], file.filename)

    except:
        print("Error occurred while attempting upload")
        return False