import json
import logging
from dataclasses import dataclass
from io import BytesIO

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from mypy_boto3_s3 import ServiceResource
from mypy_boto3_s3.service_resource import Bucket
from pandas import DataFrame

from app.settings import settings

logging.getLogger("botocore").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
log = logging.getLogger(__name__)


@dataclass
class AWS:
    def __post_init__(self):
        log.debug("Initializing AWS connection...")
        self.client: BaseClient = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_DEFAULT_REGION,
            endpoint_url=settings.AWS_ENDPOINT_URL,
        )
        self.resource: ServiceResource = boto3.resource(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_DEFAULT_REGION,
            endpoint_url=settings.AWS_ENDPOINT_URL,
        )
        self.bucket: Bucket = self.resource.Bucket(settings.AWS_BUCKET_NAME)
        log.debug("Initialized AWS connection!")

    def save_to_json(self, data: dict, path: str, file_name: str):
        log.debug(f"Saving {file_name}.json @ {path}")
        self.client.put_object(
            Body=json.dumps(data),
            Bucket=settings.AWS_BUCKET_NAME,
            Key=f"{path}/{file_name}.json",
        )

    def read_from_json(self, file_path: str) -> dict:
        return json.loads(
            self.client.get_object(Bucket=settings.AWS_BUCKET_NAME, Key=file_path)
            .get("Body")
            .read()
            .decode("utf-8"),
        )

    def save_to_parquet(self, df: DataFrame, path: str, file_name: str):
        log.debug(f"Saving {file_name}.parquet @ {path}")

        # Write DataFrame to a Parquet file (in memory)
        parquet_buffer = BytesIO()
        df.to_parquet(parquet_buffer)

        # Seek to start of the buffer
        parquet_buffer.seek(0)

        # Upload Parquet file to S3
        self.client.put_object(
            Body=parquet_buffer.getvalue(),
            Bucket=settings.AWS_BUCKET_NAME,
            Key=f"{path}/{file_name}.parquet",
        )

    def list_files(self, path: str) -> list:
        return [obj.key for obj in list(self.bucket.objects.filter(Prefix=path))]

    def file_exists(self, file_path: str) -> bool:
        try:
            self.client.head_object(Bucket=settings.AWS_BUCKET_NAME, Key=file_path)
            return True
        except ClientError:
            return False
