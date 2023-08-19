.PHONY: build airflow-init up-db uu-pgadmin up-scheduler up-webserver start stop

help:
	@echo "Available commands:"
	@echo "  make build        - Build the Docker image for airflow with custom packages"
	@echo "  make airflowdb    - Start airflow-db service in the background"
	@echo "  make warehousedb  - Start warehouse db service in the background"
	@echo "  make pgadmin      - Start pgadmin service in the background"
	@echo "  make airflow-init - Start airflow-init service to setup airflow image and create users"
	@echo "  make scheduler    - Start airflow-scheduler service in the background"
	@echo "  make webserver    - Start airflow-webserver service in the background"
	@echo "  make start        - Build the image and start all services sequentially"
	@echo "  make stop         - Stop and remove the Docker services"


build:
	docker build --build-arg DOCKER_UID=`id -u` --rm -t app-airflow-dbt .

# Start services in sequence
airflowdb:
	docker-compose up -d airflowdb

warehousedb:
	docker-compose up -d db

pgadmin:
	docker-compose up -d pgadmin

airflow-init:
	docker-compose up airflow-init

scheduler:
	docker-compose up -d airflow-scheduler

webserver:
	docker-compose up -d airflow-webserver

# Start all services sequentially
start: build airflowdb warehousedb pgadmin airflow-init  scheduler webserver

# Stop and remove the Docker services
stop:
	docker-compose down -v
