
''' Local Modules import '''
from services.s3_client_service import S3ClientService
from services.s3_object_service import S3ObjectService
from utils.constants import S3_BUCKET_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_DEFAULT_REGION
from utils.utils import list_all_objects, delete_objects_in_batches


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
    data_bucket_obects = list_all_objects(s3_object_service)

    print(f'Total Objects = {len(data_bucket_obects)}')
    # for el in data_bucket_obects :
    #     print(el)

    ''' Deleting Objects where meta data have prime = 1 '''
    objects_to_delete = [el['Key']
                         for el in data_bucket_obects if el['Metadata']['prime'] != '1']

    if delete_objects_in_batches(s3_object_service=s3_object_service, objects_to_delete=objects_to_delete):
        print("Objects deleted successfully")

    data_bucket_obects = list_all_objects(s3_object_service)
    print(f'Objects left = {len(data_bucket_obects)}')


''' Code execution starts from here '''
if __name__ == "__main__":
    main()
