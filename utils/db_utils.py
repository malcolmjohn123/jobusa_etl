import psycopg2
import pandas as pd
import logging
from pandas.io import sql
from typing import List, Dict, Any, Union

class DBUtils:
    """
    A utility class for simplifying database interactions using psycopg2 and pandas.
    """

    def __init__(self, logger: logging.Logger = None, config: Union[str, Dict[str, str]] = None):
        """
        Initialize a DBUtils instance.

        Args:
            logger (logging.Logger): Optional logger instance for logging messages.
            config (Union[str, Dict[str, str]]): Configuration parameters for the database connection.
        """
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.server_params = config

    def get_connection(self):
        """
        Create and return a database connection using psycopg2.

        Returns:
            psycopg2.extensions.connection: A psycopg2 database connection.
        """
        return psycopg2.connect(
            host=self.server_params["host"],
            database=self.server_params["database"],
            user=self.server_params["user"],
            password=self.server_params["password"],
            port=self.server_params["port"]
        ) 
    
    def dataframe_to_tables(self, dataframes: Dict, schema: str):
        """
        Load DataFrames into PostgreSQL tables.

        Args:
            dataframes (Dict): A dictionary of table names as keys and DataFrames as values.
            schema (str): The schema where the tables should be created.
        """
        db_url = f"postgresql://{self.server_params['user']}:{self.server_params['password']}@" \
                 f"{self.server_params['host']}:{self.server_params['port']}/{self.server_params['database']}"

        for table_name, df in dataframes.items():
            try:
                sql.to_sql(df, name=table_name, schema=schema, con=db_url, if_exists='replace', index=False)
            except Exception as e:
                self.logger.exception(f"An error occurred during loading DataFrame to table {table_name}: {e}")

    def execute_queries(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute SQL queries in the database.

        Args:
            query (str): The SQL query to execute.

        Returns:
            List[Dict[str, Any]]: A list of query results (dicts).
        """
        connection = self.get_connection()

        try:
            with connection.cursor() as cur:
                cur.execute(query)
                connection.commit()
        except psycopg2.Error:
            self.logger.exception("Database error")
            raise
        finally:
            connection.close()

    def copy_to_db_and_return_affected_count(self, copy_query, file) -> int:
        """
        Execute a COPY command to load data from a file into the database.

        Args:
            copy_query (str): The COPY command query.
            file: The file object to read data from.

        Returns:
            int: The number of affected rows.
        """
        connection = self.get_connection()    

        try:
            with connection.cursor() as cur:
                cur.copy_expert(sql=copy_query, file=file)
                affected_rows = cur.rowcount
                connection.commit()
                return affected_rows
        except psycopg2.Error:
            connection.rollback()
            self.logger.exception("Database error")
            raise
        finally:
            connection.close()
    

    def insert_to_db_and_return_affected_count(self, insert_data, insert_query) -> int:
        """
        Execute an INSERT command to insert data into the database.

        Args:
            insert_data: Data to be inserted.
            insert_query (str): The INSERT command query.

        Returns:
            int: The number of affected rows.
        """
        connection = self.get_connection()
        
        try:
            with connection.cursor() as cur:
                cur.executemany(insert_query, insert_data)
                affected_rows = cur.rowcount
                connection.commit()
                return affected_rows
        except psycopg2.Error:
            connection.rollback()
            self.logger.exception("Database error")
            raise
        finally:
            connection.close()
