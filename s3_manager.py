import logging
import boto3
import botocore
from botocore.exceptions import ClientError
import requests


class s3Manager:

    def __init__(self):
        self.__s3_resource = boto3.resource('s3', region_name='us-east-1')
        self.__s3_client = boto3.client('s3', region_name='us-east-1')
        self.ARTIST_IMAGE_BUCKET_NAME = 's3500659-artist-images'

    def check_bucket_exists(self, bucket_name):
        exists = True
        try:
            self.__s3_resource.meta.client.head_bucket(
                Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            if error_code == '404':
                exists = False
        return exists

    def count_objects_in_bucket(self, bucket_name):
        bucket = self.__s3_resource.Bucket(bucket_name)

        count_obj = 0
        for i in bucket.objects.all():
            count_obj = count_obj + 1

    def check_file_exist(self, bucket, key):
        try:
            self.__s3_resource.Object(bucket, key).load()
        except ClientError as e:
            return int(e.response['Error']['Code']) != 404
        print("checking key {}".format(key))
        return True

    def upload_image_url_to_bucket(self, bucket_name, file_name, url):
        bucket_name_to_upload_image_to = bucket_name
        s3_image_filename = file_name
        internet_image_url = url

        for bucket in self.__s3_resource.buckets.all():
            if bucket.name == bucket_name_to_upload_image_to:
                print('Uploading image: {}'.format(file_name))
                good_to_go = True

        if not good_to_go:
            print('Bucket not found, check IAM permission')

        req_for_image = requests.get(internet_image_url, stream=True)
        file_object_from_req = req_for_image.raw
        req_data = file_object_from_req.read()

        self.__s3_resource.Bucket(bucket_name_to_upload_image_to).put_object(
            Key=s3_image_filename, Body=req_data)

    def create_bucket(self, bucket_name, region=None):
        """Create an S3 bucket in a specified region

            If a region is not specified, the bucket is created in the S3 default
            region (us-east-1).

            :param bucket_name: Bucket to create
            :param region: String region to create bucket in, e.g., 'us-west-2'
            :return: True if bucket created, else False
            """

        # Create bucket
        try:
            if region is None:
                self.__s3_resource.create_bucket(Bucket=bucket_name)
                return True
            else:
                location = {'LocationConstraint': region}
                self.__s3_resource.create_bucket(Bucket=bucket_name,
                                                 CreateBucketConfiguration=location)
                return True
        except ClientError as e:
            logging.error(e)
            return False
