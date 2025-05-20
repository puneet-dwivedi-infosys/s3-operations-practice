
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# default region for the aws deployment
DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")

AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

S3_BUCKET_NAME = "data-bucket-1746002001281"
