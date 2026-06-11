import boto3
from botocore.exceptions import BotoCoreError, ClientError

from src.utils.paths import (
    LOCALSTACK_ENDPOINT_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
)


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=LOCALSTACK_ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )


def check_localstack_connection(bucket_name: str) -> None:
    try:
        s3_client = get_s3_client()

        buckets = s3_client.list_buckets()
        existing_buckets = [bucket["Name"] for bucket in buckets.get("Buckets", [])]

        if bucket_name not in existing_buckets:
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"Bucket created: {bucket_name}")
        else:
            print(f"Bucket already exists: {bucket_name}")

        print("LocalStack connection validated successfully.")

    except (BotoCoreError, ClientError) as error:
        raise ConnectionError(
            "Could not connect to LocalStack. "
            "Check if Docker and LocalStack are running."
        ) from error