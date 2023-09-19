
# USAJOBS Data ETL Project

This repository contains an end-to-end ETL (Extract, Transform, Load) pipeline for extracting job data from the USAJOBS API, transforming it, loading it into a PostgreSQL data warehouse, and generating insights using dbt. The project is orchestrated using Apache Airflow and is containerized using Docker.



## Folder Structure

```bash
  usajobs_etl/  
├── dags/    
│   ├── etl_dag.py
├── dbt/
│   ├── data
│   ├── models/
│   ├── dbt_project.yml
│   ├── profiles.yml
├── extraction/          
│   ├──api_extract.py
├── utils/          
│   ├── __init__.py
│   ├── api_utils.py
│   ├── db_utils.py
│   ├── config_utils.py
│   ├── dbt_utils.py
│   ├── log_utils.py
├── docker-compose.yml
├── Dockerfile          
├── setup.py
├── Makefile
```
## Pipeline Overview

**Data Extraction**: The api_extract.py script in the extraction/ folder extracts data from an API and loads it into the src schema of the PostgreSQL data warehouse. Two tables, job_postings and user_area, are populated with relevant data.

**Staging**: Extracted data is moved to the stg schema, where data cleaning and transformation are performed. Distinct records are generated, and appropriate data types are applied.

**Lookups**: Lookup tables like travel are created as seeds, containing reference data for code-to-description mapping.

**Insights Generation**: Views containing insights and analytics are generated in the public schema.

**Airflow DAGs**: The etl_dag.py DAG definition in the dags/ folder orchestrates the ETL process, scheduling the extraction, staging, lookup, and insights tasks.

**Dockerization**: The entire pipeline is containerized using Docker, including services like Airflow, PostgreSQL, and pgAdmin.

The staging models creation and insights generation are done using dbt. Stagings are materiazed as tables and insights are materialized as views.

![jobusa2 drawio (3)](https://github.com/malcolmjohn123/jobusa_etl/assets/20333666/7701ef5f-87e7-4c0f-8496-ae3542f8fcf7)

And as mentioned above the whole process is orchestrated and run in airflow scheduler. Prcoessing is set to run daily. Below is DAG that is created

![ETL DAG2](https://github.com/malcolmjohn123/jobusa_etl/assets/20333666/a3e77779-2e24-46a6-bd73-3c29723df22b)


The data pipeline is designed to do full loading as extraction script extracts full data every day using the API.
## Run Locally

To run the project locally

You need to have installed following

- Docker
- Python

Clone the project

```bash
  git clone https://github.com/malcolmjohn123/jobusa_etl.git
```

Go to the project directory

```bash
  cd jobusa_etl
```

Change the .env.example file to .env file and set the environemnt variables. For ease I have already the set the necessary variables. You just need to set the veraibles below

```bash
  API_USER_AGENT = 
  API_AUTHORIZATION_KEY= 
```

Start the services using Makefile

```bash
  make start
```
Once the service is tarted  visit the url below to access airflow ui. You can use the username = **admin** and pwd = **airflow** set in .env.example file. access the airflowUI and start dag

```bash
  http://localhost:8081/
```

To access the pgadmin and to start dag visit the url. Login to pogadmin ui with useremail = **admin@admin.com** and pwd = **admin**. Addd server with credentials host = **db**, port = **5432**, username=**postgres**, pwd=**postgres**.These credentials are set in .env.example file.

```bash
  http://localhost:8080/
```

## Description about running the application

So all the servies requried are containerized. For this application we will have 5 services running

- airflow database
- airflow scheduler
- airflow webserver for UI
- postgres server for datawarehouse
- pgadmin to connect postgres server

So all these services are run in containers through docker-compose. To be able to run these services with ease Makefile has been created. To get familiar with commands type **make help** and hit enter and following will appear

```bash
  Available commands:
  make build        - Build the airflow Docker image with custom packages
  make airflowdb    - Start airflow-db service in the background
  make warehousedb  - Start warehouse db service in the background
  make pgadmin      - Start pgadmin service in the background
  make airflow-init - Start airflow-init service to setup airflow image and create users
  make scheduler    - Start airflow-scheduler service in the background
  make webserver    - Start airflow-webserver service in the background
  make start        - Build the image and start all services sequentially
  make stop         - Stop and remove the Docker services
```

To start all the services type **make start** and hit enter. If some how services fail to start while using makefile start. Stop all the services running using **make stop**. And follow the sequential order of service you see while getting with make help and start one by one.
