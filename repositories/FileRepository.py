import logging
from importlib.metadata import metadata
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

class FileRepository:
    def __init__(self):
        self.bucket_name = os.getenv("S3_BUCKET")
        self.region = "us-east-1"
        self.access_key = os.getenv("AWS_ACCESS_KEY")
        self.secret_key = os.getenv("AWS_SECRET_KEY")

    def upload_file(self, file_name, object_name=None):
        """Upload a file to an S3 bucket


        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3_client = boto3.client(
            service_name='s3',
            region_name=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )
        try:
            print(f"Uploading {file_name} to {self.bucket_name}/{object_name}...")
            response = s3_client.upload_file(
                file_name,
                self.bucket_name,
                object_name,
                ExtraArgs={'ContentType': 'image/jpeg'}
            )
            pprint(response)
        except ClientError as e:
            logging.error(e)
            return False
        return response