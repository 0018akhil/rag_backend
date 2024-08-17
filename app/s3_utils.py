import boto3
from botocore.exceptions import ClientError
import logging
from dotenv import load_dotenv
import os

load_dotenv()

s3_client = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

def upload_file_to_s3(file, object_name):
    try:
        s3_client.upload_fileobj(file, BUCKET_NAME, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True