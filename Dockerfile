FROM apache/airflow:2.1.1-python3.8

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir .