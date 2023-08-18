import os
import subprocess

from typing import List
from .log_utils import get_logger

logger = get_logger('DATA_PIPELINE_LOGGER')


def run_dbt_command(dbt_cmds:List):
    """
    Run a dbt command using subprocess.
    
    Args:
        command (str): The dbt command to run.
        
    Returns:
        bool: True if the command ran successfully, False otherwise.
    """
    for command in dbt_cmds:
        try:
            subprocess.run(command, shell=True, check=True)
            logger.info("DBT command executed sucessfully")
            
        except subprocess.CalledProcessError as e:
            logger.error("Error executing dbt command: %s", e)
            return False
    
    return True

