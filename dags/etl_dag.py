from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(5)
}


etl_dag = DAG(
    'jobpost_ingestion',
    default_args=default_args,
    description='Extracts data from API, transforms it into warehouse and generated insights',
    schedule_interval=timedelta(days=1),
    catchup=False
)


# Task 1: Extract raw data from the API
task_1 = BashOperator(
    task_id='extract_raw_data',
    bash_command='python /opt/airflow/extraction/usajob_api_extract.py',
    dag=etl_dag,
)

# Task 2: Create staging tables using dbt
task_2 = BashOperator(
    task_id='staging_tables_create',
    bash_command='dbt run --profiles-dir=/opt/airflow/dbt --project-dir=/opt/airflow/dbt --select staging',
    dag=etl_dag,
)

# Task 3: Seed lookup tables using dbt
task_3 = BashOperator(
    task_id='lookup_create',
    bash_command='dbt seed --profiles-dir=/opt/airflow/dbt --project-dir=/opt/airflow/dbt',
    dag=etl_dag,
)

# Task 4: Generate insights using dbt
task_4 = BashOperator(
    task_id='insights_generation',
    bash_command='dbt run --profiles-dir=/opt/airflow/dbt --project-dir=/opt/airflow/dbt --select public',
    dag=etl_dag,
)

# Task dependencies
task_1 >> task_2
task_2 >> task_4
task_3 >> task_4