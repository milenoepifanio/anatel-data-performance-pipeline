import boto3
from botocore.exceptions import ClientError
from pathlib import Path

from src.utils.paths import (
    STAGING_LONG_FILES_DIR,
    LOCALSTACK_ENDPOINT_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    BUCKET_NAME,
    S3_PREFIX,
)

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=LOCALSTACK_ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )


def create_bucket_if_not_exists(s3_client, bucket_name: str) -> None:
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket já existe: {bucket_name}")

    except ClientError:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket criado: {bucket_name}")


def list_local_parquet_files(source_dir: Path) -> list[Path]:
    parquet_files = list(source_dir.rglob("*.parquet"))

    if not parquet_files:
        raise FileNotFoundError(
            f"Nenhum arquivo .parquet encontrado em: {source_dir}"
        )

    return parquet_files


def upload_parquet_files_to_s3(
    s3_client,
    source_dir: Path,
    bucket_name: str,
    s3_prefix: str,
) -> list[str]:
    uploaded_files = []

    parquet_files = list_local_parquet_files(source_dir)

    for file_path in parquet_files:
        relative_path = file_path.relative_to(source_dir)

        s3_key = (
            f"{s3_prefix}/{relative_path}"
            .replace("\\", "/")
        )

        s3_client.upload_file(
            Filename=str(file_path),
            Bucket=bucket_name,
            Key=s3_key,
        )

        s3_uri = f"s3://{bucket_name}/{s3_key}"
        uploaded_files.append(s3_uri)

        print(f"Upload realizado: {file_path} -> {s3_uri}")

    return uploaded_files


def main():
    s3_client = get_s3_client()

    create_bucket_if_not_exists(
        s3_client=s3_client,
        bucket_name=BUCKET_NAME,
    )

    uploaded_files = upload_parquet_files_to_s3(
        s3_client=s3_client,
        source_dir=STAGING_LONG_FILES_DIR,
        bucket_name=BUCKET_NAME,
        s3_prefix=S3_PREFIX,
    )

    print("\nResumo do upload:")
    print(f"Bucket: {BUCKET_NAME}")
    print(f"Prefixo S3: {S3_PREFIX}")
    print(f"Arquivos enviados: {len(uploaded_files)}")


if __name__ == "__main__":
    main()