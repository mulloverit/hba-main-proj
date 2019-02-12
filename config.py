import os

# AWS S3 specific
S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
S3_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION = 'http://{}s3.amazonaws.com/'.format(S3_BUCKET)

# Flask application general
SECRET_KEY = 'faking_it_for_now' # use os.urandom(32) ?
