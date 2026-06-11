from src.ingestion.refactor_scraping_class import AnatelPerformanceScraper
from src.processing.silver_long_transformer import AnatelLongPySparkTransformer
from src.processing.upload_parquet_to_s3 import upload_parquet_files_to_s3

from src.orchestration.environment import check_environment_variables
from src.orchestration.localstack import check_localstack_connection
from src.orchestration.dbt_runner import run_dbt_models

from src.utils.paths import (
    RAW_DIR,
    STAGING_LONG_FILES_DIR,
    BUCKET_NAME,
    S3_PREFIX,
    create_directories,
)


def run_ingestion() -> None:
    print("Starting ingestion...")

    scraper = AnatelPerformanceScraper()
    scraper.run()

    print("Ingestion completed.")


def run_silver_transformation() -> None:
    print("Starting Silver transformation...")

    transformer = AnatelLongPySparkTransformer()

    result = transformer.transform_raw_to_long_parquet(
        raw_path=str(RAW_DIR),
        output_path=str(STAGING_LONG_FILES_DIR),
    )

    print(result)
    print("Silver transformation completed.")


def run_s3_upload() -> None:
    print("Starting upload to S3 LocalStack...")

    upload_parquet_files_to_s3(
        local_path=str(STAGING_LONG_FILES_DIR),
        bucket_name=BUCKET_NAME,
        s3_prefix=S3_PREFIX,
    )

    print("Upload to S3 completed.")


def main() -> None:
    create_directories()

    check_environment_variables()

    check_localstack_connection(bucket_name=BUCKET_NAME)

    run_ingestion()

    run_silver_transformation()

    run_s3_upload()

    run_dbt_models()

    print("Pipeline executed successfully.")


if __name__ == "__main__":
    main()