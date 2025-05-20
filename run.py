
''' Local Modules import '''
from src.services.s3_client_service import S3ClientService
from src.services.s3_object_service import S3ObjectService
from src.utils.constants import S3_BUCKET_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_DEFAULT_REGION
from src.utils.utils import list_all_objects, delete_objects_in_batches


def main():
    ''' Creating S3 Client '''
    s3_client = S3ClientService(
        access_key=AWS_ACCESS_KEY,
        secret_key=AWS_SECRET_KEY,
        region=AWS_DEFAULT_REGION
    ).get_s3_client()

    ''' S3 Object Service '''
    s3_object_service = S3ObjectService(s3_client, S3_BUCKET_NAME)

    ''' 
    S3 operations 
    '''
    
    ''' Fetching all the objects '''

    # deleting object by meta data
    s3_object_service.delete_objects_by_meta_data({'prime' : '1'})

    # deleting object by key
    s3_object_service.delete_objects_by_tags({'category':'odd'})

    
''' Code execution starts from here '''
if __name__ == "__main__":
    main()
