import os
import sys

from src.utils.paths import JAVA_HOME, SPARK_HOME, HADOOP_HOME


def configure_environment() -> None:
    os.environ["JAVA_HOME"] = str(JAVA_HOME)
    os.environ["SPARK_HOME"] = str(SPARK_HOME)
    os.environ["HADOOP_HOME"] = str(HADOOP_HOME)
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    os.environ["PATH"] = (
        str(HADOOP_HOME / "bin")
        + os.pathsep
        + str(JAVA_HOME / "bin")
        + os.pathsep
        + str(SPARK_HOME / "bin")
        + os.pathsep
        + os.environ.get("PATH", "")
    )
