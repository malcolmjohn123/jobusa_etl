import os
from dotenv import load_dotenv
from typing import Dict
from .dbt_utils import logger

class Config:
    """
    Configuration class for managing environment variables and retrieving configuration settings.
    """

    load_dotenv()  # Load environment variables from .env file

    @staticmethod
    def get_api_headers() -> Dict:
        """
        Retrieve API headers from environment variables.

        Returns:
            dict: A dictionary containing API headers, including Host, User-Agent, and Authorization-Key.
                  None if any required environment variable is missing.
        """
        try:
            api_host = os.environ.get("API_HOST")
            api_user_agent = os.environ.get("API_USER_AGENT")
            api_auth_key = os.environ.get("API_AUTHORIZATION_KEY")

            return {
                "Host": api_host,
                "User-Agent": api_user_agent,
                "Authorization-Key": api_auth_key
            }
        except KeyError:
            logger.exception("Error while reading API config")
            return None

    @staticmethod
    def get_db_config(section: str = 'POSTGRES') -> Dict:
        """
        Retrieve database configuration settings from environment variables.

        Args:
            section (str): The section of the database configuration to retrieve.

        Returns:
            dict: A dictionary containing database configuration settings,
                  including host, database name, user, password, and port.
                  None if any required environment variable is missing.
        """
        try:
            db_host = os.environ.get("POSTGRES_HOST")
            db_database = os.environ.get("POSTGRES_DATABASE")
            db_user = os.environ.get("POSTGRES_USER")
            db_password = os.environ.get("POSTGRES_PWD")
            db_port = os.environ.get("POSTGRES_PORT")

            return {
                "host": db_host,
                "database": db_database,
                "user": db_user,
                "password": db_password,
                "port": db_port
            }
        except KeyError:
            logger.exception("Error while reading DB config")
            return None
