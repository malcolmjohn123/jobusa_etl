.PHONY: build airflow-init up-db uu-pgadmin up-scheduler up-webserver start stop

help:
	@echo "Available commands:"
	@echo "  make build        - Build the Docker image for airflow with custom packages"
	@echo "  make up-airflowdb   - Start airflow-db service in the background"
	@echo "  make up-db        - Start warehouse db service in the background"
	@echo "  make up-pgadmin   - Start pgadmin service in the background"
	@echo "  make airflow-init - Start airflow-init service to setup airflow image and create users"
	@echo "  make up-scheduler - Start airflow-scheduler service in the background"
	@echo "  make up-webserver - Start airflow-webserver service in the background"
	@echo "  make start        - Build the image and start all services sequentially"
	@echo "  make stop         - Stop and remove the Docker services"


build:
	sudo docker build -t app-airflow-dbt .

# Start services in sequence
up-airflowdb:
	sudo docker-compose up -d airflowdb

up-db:
	sudo docker-compose up -d db

up-pgadmin:
	sudo docker-compose up -d pgadmin

airflow-init:
	sudo docker-compose up airflow-init

up-scheduler:
	sudo docker-compose up -d airflow-scheduler

up-webserver:
	sudo docker-compose up -d airflow-webserver

# Start all services sequentially
start: build up-airflowdb up-db up-pgadmin airflow-init  up-scheduler up-webserver

# Stop and remove the Docker services
stop:
	sudo docker-compose down -v
