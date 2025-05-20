
from src.utils.constants import DEFAULT_REGION


class S3BucketService():

    def __init__(self, s3_client):
        self.__s3_client = s3_client

    def create_bucket(self, bucket_name, region_name=DEFAULT_REGION):
        try:
            self.__s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': region_name
                },
            )
            print("Bucket created successfully")
        except Exception as e:
            if "BucketAlreadyOwnedByYou" in str(e):
                print("Bucket already exists")
            else:
                print(f"Error Creating Bucket, {e}")
