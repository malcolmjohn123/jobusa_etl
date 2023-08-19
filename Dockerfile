FROM apache/airflow:2.1.1-python3.8

WORKDIR /app

COPY utils /app/utils

COPY setup.py /app/setup.py

RUN pip install --upgrade pip

RUN pip install .

USER root

ARG DOCKER_UID
ARG DOCKER_GID
RUN \
    : "${DOCKER_UID:?Build argument DOCKER_UID needs to be set and non-empty. Use 'make build' to set it automatically.}" \
    && usermod -u ${DOCKER_UID} airflow \
    && echo "Set airflow's uid to ${DOCKER_UID}"

USER airflow
