''' MOdule imports '''
import os
import boto3
import pytest
from moto import mock_aws  

''' local modules '''
from src.services.s3_object_service import S3ObjectService
from src.utils.constants import DEFAULT_REGION, S3_BUCKET_NAME

@pytest.fixture(scope="function")
def s3_service():
    with mock_aws():
        session = boto3.session.Session(
            aws_access_key_id="FAKE",
            aws_secret_access_key="FAKE",
            region_name=DEFAULT_REGION
        )

        client = session.client("s3", region_name=DEFAULT_REGION)
        client.create_bucket(
            Bucket=S3_BUCKET_NAME,
            CreateBucketConfiguration={'LocationConstraint': DEFAULT_REGION}
        )
        service = S3ObjectService(client, S3_BUCKET_NAME)
        yield service

class TestS3ObjectService:

    def test_upload_object(self, s3_service):
        result = s3_service.upload_object(
            object_key="file.txt",
            body=b"Hello, world!",
            meta_data={"env": "test"},
            tags="type=test"
        )
        assert result is True

        objects = s3_service.list_objects()
        assert len(objects) == 1
        assert objects[0]["Key"] == "file.txt"

    def test_get_object_head(self, s3_service):
        key = "file-meta.txt"
        metadata = {"x-custom-meta": "abc123"}

        s3_service.upload_object(key, b"Metadata test", meta_data=metadata)

        head = s3_service.get_object_head(key)
        assert head["Key"] == key
        assert head["Metadata"] == metadata
        assert head["Bucket"] == S3_BUCKET_NAME

    def test_list_objects(self, s3_service):
        keys = ["file1.txt", "file2.txt", "file3.txt"]
        for key in keys:
            s3_service.upload_object(key, b"content")

        objects = s3_service.list_objects()
        object_keys = [obj["Key"] for obj in objects]

        assert set(object_keys) == set(keys)

    def test_delete_objects(self, s3_service):
        keys = ["delete1.txt", "delete2.txt"]
        for key in keys:
            s3_service.upload_object(key, b"to be deleted")

        success = s3_service.delete_objects(keys)
        assert success is True

        objects = s3_service.list_objects()
        assert objects == []
