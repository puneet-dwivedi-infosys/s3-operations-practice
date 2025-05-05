from .classes import DataProcessor


def is_prime(n):
    if n <= 1:
        return 0
    i = 2
    while i*i <= n:
        if n % i == 0:
            return 0
        i += 1
    return 1

def create_batches(data, batch_size=5):
    batch_data = []
    for i in range(0, len(data), batch_size):
        batch_data.append(data[i:i + batch_size])
    return batch_data

def generate_demo_objects(count):
    data = []
    for i in range(count):
        body = f'This is object {i} content'
        meta_data = {
            'number': str(i),
            'category': 'odd' if i % 2 == 1 else 'even',
            'prime': str(is_prime(i))
        }
        object_key = f'object-{i}'
        tags = f'number={i}'

        data.append({
            'body' : body,
            'meta_data' : meta_data,
            'object_key' : object_key,
            'tags' : tags
        })
    return data

def upload_demo_objects_to_s3(s3_object_service, upload_count=10):

    try:
        ''' Genrating the demo objects '''
        data = generate_demo_objects(upload_count)
        DataProcessor(data=data, data_processor=s3_object_service.upload_object)\
        .run_concurrently()
        
        print(f"{upload_count} objects uploaded successfully")
    except Exception as e:
        print(f"Error uploading object, {e}")

def delete_objects_in_batches(s3_object_service, objects_to_delete) :
    try:
        objects_to_delete_batches = create_batches(objects_to_delete, 3)
        DataProcessor(data=objects_to_delete_batches, data_processor=s3_object_service.delete_objects)\
        .run_concurrently()
        return True
    except Exception as e:
        print(f'Error deleting the object {e}')
        return False

def list_all_objects(s3_object_service):
    data_bucket_objects = s3_object_service.list_objects()

    parsed_data_bucket_objects = []

    for _object in data_bucket_objects:
        object_key = _object['Key']
        object_head = s3_object_service.get_object_head(object_key)
        parsed_data_bucket_objects.append(object_head)

    return parsed_data_bucket_objects
