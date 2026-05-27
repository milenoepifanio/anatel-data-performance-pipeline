from src.processing.silver_long_transformation import (
    AnatelLongPySparkTransformer
)

from src.utils.paths import (
    RAW_DIR,
    STAGING_LONG_FILES_DIR,
    create_directories,
)


def main():

    create_directories()

    transformer = AnatelLongPySparkTransformer()

    result = transformer.transform_raw_to_long_parquet(
        raw_path=str(RAW_DIR),
        output_path=str(STAGING_LONG_FILES_DIR),
    )

    print(result)


if __name__ == "__main__":
    main()