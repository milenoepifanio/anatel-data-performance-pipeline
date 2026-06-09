FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/hadoop
ENV LOCALSTACK_ENDPOINT_URL=http://localstack:4566
ENV AWS_ACCESS_KEY_ID=test
ENV AWS_SECRET_ACCESS_KEY=test
ENV AWS_REGION=us-east-1
ENV BUCKET_NAME=anatel-lake
ENV S3_PREFIX=silver/anatel_long

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jdk \
    curl \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["bash"]
