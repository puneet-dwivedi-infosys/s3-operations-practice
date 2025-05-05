
''' Local Modules import '''
from services.s3_client_service import S3ClientService
from services.s3_bucket_service import S3BucketService
from services.s3_object_service import S3ObjectService
from utils.utils import upload_demo_objects_to_s3
from utils.constants import S3_BUCKET_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_DEFAULT_REGION


def seed():
    ''' Creating S3 Client '''
    s3_client = S3ClientService(
        access_key=AWS_ACCESS_KEY,
        secret_key=AWS_SECRET_KEY,
        region=AWS_DEFAULT_REGION
    ).get_s3_client()

    ''' S3 Bucket creation '''
    s3_bucket_service = S3BucketService(s3_client)

    s3_bucket_service.create_bucket(bucket_name=S3_BUCKET_NAME)

    ''' Object upload '''
    s3_object_service = S3ObjectService(s3_client, S3_BUCKET_NAME)

    upload_demo_objects_to_s3(s3_object_service, upload_count=20)


''' Code execution starts from here '''
if __name__ == "__main__":
    seed()
