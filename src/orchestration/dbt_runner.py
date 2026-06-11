import subprocess

from src.utils.paths import PROJECT_ROOT


def run_dbt_models() -> None:
    print("Running dbt models...")

    result = subprocess.run(
        ["dbt", "run"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("dbt run failed.")

    print(result.stdout)
    print("dbt models executed successfully.")