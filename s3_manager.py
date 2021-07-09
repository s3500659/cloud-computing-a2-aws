import logging
import boto3
from botocore.exceptions import ClientError
import requests


class s3_manager:

    def __init__(self):
        self.__s3_client = boto3.resource('s3', region_name = 'us-east-1')

    def count_objects_in_bucket(self, bucket_name):
        bucket = self.__s3_client.Bucket(bucket_name)

        count_obj = 0
        for i in bucket.objects.all():
            count_obj = count_obj + 1


    def check_file_exist(self, bucket, key):
        try:
            self.__s3_client.Object(bucket, key).load()
        except ClientError as e:
            return int(e.response['Error']['Code']) != 404
        print("checking key {}".format(key))
        return True


    def upload_image_url_to_bucket(self, bucket_name, file_name, url):
        bucket_name_to_upload_image_to = bucket_name
        s3_image_filename = file_name
        internet_image_url = url

        for bucket in self.__s3_client.buckets.all():
            if bucket.name == bucket_name_to_upload_image_to:
                print('Uploading image: {}...'.format(file_name))
                good_to_go = True

        if not good_to_go:
            print('Bucket not found, check IAM permission')

        req_for_image = requests.get(internet_image_url, stream=True)
        file_object_from_req = req_for_image.raw
        req_data = file_object_from_req.read()

        self.__s3_client.Bucket(bucket_name_to_upload_image_to).put_object(
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
                self.__s3_client.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.__s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False

        return True
