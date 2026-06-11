from src.utils.paths import (
    LOCALSTACK_ENDPOINT_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    BUCKET_NAME,
    S3_PREFIX,
)


def check_environment_variables() -> None:
    required_values = {
        "LOCALSTACK_ENDPOINT_URL": LOCALSTACK_ENDPOINT_URL,
        "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
        "AWS_REGION": AWS_REGION,
        "BUCKET_NAME": BUCKET_NAME,
        "S3_PREFIX": S3_PREFIX,
    }

    missing_vars = [
        var_name
        for var_name, var_value in required_values.items()
        if not var_value
    ]

    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    print("Environment variables validated successfully.")