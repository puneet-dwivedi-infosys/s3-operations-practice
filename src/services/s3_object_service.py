

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
        except Exception as e:
            print(f"Error uploading the object, {e}")

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
            return object_head
        except Exception as e:
            print(f"Error getting head of the object")
            return {}

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
