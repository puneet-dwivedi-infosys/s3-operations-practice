import boto3


"""
A service class to manage and provide an authenticated S3 client.
"""


class S3ClientService:

    def __init__(self, access_key, secret_key, region="ap-south-1"):
        self.__session = boto3.session.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        self.__s3_client = self.__session.client("s3")

    def get_s3_client(self):
        return self.__s3_client
