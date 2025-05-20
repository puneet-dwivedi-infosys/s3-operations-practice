

class S3ObjectService():

    def __init__(self, s3_client, bucket_name):
        self.__s3_client = s3_client
        self.bucket_name = bucket_name

    def upload_object(self, object_key, body, meta_data={}, tags=''):
        try:
            self.__s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=body,
                Metadata=meta_data,
                Tagging=tags
            )
            return True
        except Exception as e:
            print(f"Error uploading the object, {e}")
            return False

    def multipart_upload(self, object_key, body, part_size=10):
        print("Uploading in parts..........")
        # 1. Initiating multipart upload, creating multi part upload
        mulitpart_upload_obj = self.__s3_client.create_multipart_upload(
            Bucket=self.bucket_name,
            Key=object_key
        )

        uplaodId = mulitpart_upload_obj['UploadId']

        uploaded_parts_meta_data = []

        # 2. uploading the parts
        try:
            part_number = 0
            part_uploaded = 0
            while part_uploaded < len(body):
                part_number += 1
                # taking the current chunk (substring from u)
                current_chunk = body[part_uploaded:part_uploaded+part_size]
                part_uploaded += part_size

                # upload the parst
                part_uploaded_response = self.__s3_client.upload_part(
                    Bucket=self.bucket_name,
                    Key=object_key,
                    PartNumber=part_number,
                    UploadId=uplaodId,
                    Body=current_chunk
                )
                uploaded_parts_meta_data.append({
                    'ETag': part_uploaded_response['ETag'],
                    'PartNumber': part_number,
                })
                print(f"Part - {part_number} uploaded")

            # 3. complete the multipart upload
            self.__s3_client.complete_multipart_upload(
                Bucket=self.bucket_name,
                Key=object_key,
                MultipartUpload={'Parts': uploaded_parts_meta_data},
                UploadId=uplaodId,
            )
        except Exception as e:
            # aborting the multi part upload
            self.__s3_client.abort_multipart_upload(
                Bucket=self.bucket_name,
                Key=object_key,
                UploadId=uplaodId
            )
            print(f"Error in uploading multipart, {e}")

    def list_objects(self):
        try:
            paginator = self.__s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=self.bucket_name)

            objects = []
            for page in page_iterator:
                contents = page.get('Contents', [])
                objects.extend(contents)

            return objects
        except Exception as e:
            print(f'Error in listing objects from the bucket, {e}')
            return []

    def get_object_head(self, object_key):
        try:
            object_head = self.__s3_client.head_object(
                Bucket=self.bucket_name, Key=object_key)
            return {
                'Key': object_key,
                'Metadata': object_head['Metadata'],
                'Bucket': self.bucket_name
            }
        except Exception as e:
            print(f"Error getting head of the object")
            return {}

    def get_object_tags(self, object_key):
        response = self.__s3_client.get_object_tagging(
            Bucket=self.bucket_name,
            Key=object_key
        )
        return response['TagSet']

    def delete_objects(self, object_keys):
        if len(object_keys) <= 0:
            return True
        try:
            self.__s3_client.delete_objects(
                Bucket=self.bucket_name,
                Delete={
                    'Objects': [{'Key': key} for key in object_keys],
                    'Quiet': True
                }
            )
            return True
        except Exception as e:
            print(f'Error deleting the objects')
            return False

    def list_objects_with_tags(self):
        data_bucket_objects = self.list_objects()

        parsed_data_bucket_tags = []

        for _object in data_bucket_objects:
            object_key = _object['Key']
            object_tags = self.get_object_tags(object_key)
            
            parsed_data_bucket_tags.append({
                'Key': object_key,
                'Tags': object_tags
            })

        return parsed_data_bucket_tags

    def list_objects_with_meta_data(self):
        data_bucket_objects = self.list_objects()

        parsed_data_bucket_objects = []

        for _object in data_bucket_objects:
            object_key = _object['Key']
            object_head = self.get_object_head(object_key)            
            parsed_data_bucket_objects.append(object_head)

        return parsed_data_bucket_objects

    def delete_objects_by_meta_data(self, meta_data):
        object_list = self.list_objects_with_meta_data()
        print("Object Before deleting -", len(object_list))

        objects_to_delete = []
        for _object in object_list:

            _object_meta_data = _object['Metadata']
            include_ = True

            # for each meta data in condition if object have that if does not make include as false
            for meta_data_key, meta_data_value in meta_data.items():
                if _object_meta_data.get(meta_data_key, "") != meta_data_value:
                    include_ = False

            if include_:
                objects_to_delete.append(_object['Key'])

        print("Deleting object where meta_data =", meta_data)
        self.delete_objects(objects_to_delete)

        print("Object After deleting - ", len(object_list)-len(objects_to_delete))

    def delete_objects_by_tags(self, tags):
        object_list = self.list_objects_with_tags()
        print("Objects before deleting -", len(object_list))

        objects_to_delete = []

        for _object in object_list:
            object_tags = {tag['Key']: tag['Value'] for tag in _object['Tags']}
            include_ = True

            # Check if all provided tags match the object's tags
            for tag_key, tag_value in tags.items():
                if object_tags.get(tag_key, "") != tag_value:
                    include_ = False
                    break

            if include_:
                objects_to_delete.append(_object['Key'])

        print("Deleting objects where tags =", tags)
        self.delete_objects(objects_to_delete)

        print("Objects after deleting -", len(object_list) - len(objects_to_delete))
