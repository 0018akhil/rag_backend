import boto3
from botocore.exceptions import ClientError
import logging
from ..core.config import settings

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client('s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.bucket_name = settings.S3_BUCKET_NAME

    def upload_file_to_s3(self, file, object_name):
        try:
            self.s3_client.upload_fileobj(file, self.bucket_name, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def download_file_from_s3(self, object_name, file_name):
        try:
            self.s3_client.download_file(self.bucket_name, object_name, file_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def delete_file_from_s3(self, object_name):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True