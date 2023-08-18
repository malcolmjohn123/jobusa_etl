import json
import pandas as pd
import tempfile

from datetime import datetime
from typing import Dict
from utils.api_utils import get_api_data
from utils.dbt_utils import logger
from utils.db_utils import DBUtils
from utils.config_utils import Config


def extract(keyword:str ='Data Engineering', page:int =1):
    """
    Extract job data from the USAJobs API.

    Args:
        keyword (str): The search keyword for job data. Defaults to 'Data Engineering'.
        page (int): The page number to start extraction. Defaults to 1.

    Returns:
        str or None: The path to the temporary JSON file containing extracted data, or None in case of error.
    """
    logger.info(f'Extracting data for Keyword: "{keyword}"')

    headers = Config.get_api_headers()
    url = 'https://data.usajobs.gov/api/Search'
    params = {
    "Keyword": keyword,
    "Page": page,
    'ResultsPerPage': 500
    }

    fd, file_path = tempfile.mkstemp(prefix =f'jobsusa', suffix=f'.json')
    data = []

    try:
        while True:
            
            response = get_api_data(url, headers, params, logger)
            data.extend(response["SearchResult"]["SearchResultItems"])
        
            if page > int(response["SearchResult"]["UserArea"]["NumberOfPages"]):
                break
            
            logger.info(f'Page {page} extracted')
            page = page + 1
        
        logger.info(f'Page extraction completed and writing the data into temporary file')
        with open(file_path, mode='w') as file:
            json.dump(data, file)

        return file_path
    
    except Exception as e:
        logger.error(f"An error occurred during data extraction: {e}")
        return 


def src_load(file_path:str, schema:str = 'src'):
    """
    Load parsed job data into the database.

    Args:
        file_path (str): The path to the JSON file containing parsed job data.
        schema (str): The database schema to use. Defaults to 'src'.
    """
    logger.info(f'Starting transformation process\nReading data from temporary file')
    with open(file_path, mode='r') as file:
        data = json.load(file)

    parsed_jobs_data = []
    parsed_user_area_data = []

    logger.info(f'Parsing data for job_postings and user_area')
    try:
        for result in data:
                
                job_data = {
                    "MatchedObjectId":result["MatchedObjectId"],
                    "PositionID":result["MatchedObjectDescriptor"]["PositionID"],
                    "PositionTitle": result["MatchedObjectDescriptor"]["PositionTitle"],
                    "PositionURI": result["MatchedObjectDescriptor"]["PositionURI"],
                    "ApplyURI": result["MatchedObjectDescriptor"]["ApplyURI"][0],
                    "PositionLocationDisplay": result["MatchedObjectDescriptor"]["PositionLocationDisplay"],
                    "OrganizationName": result["MatchedObjectDescriptor"]["OrganizationName"],
                    "DepartmentName": result["MatchedObjectDescriptor"]["DepartmentName"],
                    "MinimumRange":result["MatchedObjectDescriptor"]["PositionRemuneration"][0]["MinimumRange"],
                    "MaximumRange":result["MatchedObjectDescriptor"]["PositionRemuneration"][0]["MaximumRange"],
                    "RateIntervalCode":result["MatchedObjectDescriptor"]["PositionRemuneration"][0]["RateIntervalCode"],
                    "Description":result["MatchedObjectDescriptor"]["PositionRemuneration"][0]["Description"],
                    "PositionStartDate": result["MatchedObjectDescriptor"]["PositionStartDate"],
                    "PositionEndDate": result["MatchedObjectDescriptor"]["PositionEndDate"],
                    "PublicationStartDate": result["MatchedObjectDescriptor"]["PublicationStartDate"],
                    "ApplicationCloseDate": result["MatchedObjectDescriptor"]["ApplicationCloseDate"],
                    "load_date":datetime.now()
                    
                }
                parsed_jobs_data.append(job_data)
            
                user_area_data = {
                    "MatchedObjectId":result["MatchedObjectId"],
                    "LowGrade":result["MatchedObjectDescriptor"]["UserArea"]["Details"]["LowGrade"],
                    "HighGrade":result["MatchedObjectDescriptor"]["UserArea"]["Details"]["HighGrade"],
                    "PromotionPotential":result["MatchedObjectDescriptor"]["UserArea"]["Details"]["PromotionPotential"],
                    "SubAgencyName": result["MatchedObjectDescriptor"]["UserArea"]["Details"].get("SubAgencyName"),
                    "Relocation":result["MatchedObjectDescriptor"]["UserArea"]["Details"]["Relocation"],
                    "TotalOpenings":result["MatchedObjectDescriptor"]["UserArea"]["Details"].get("TotalOpenings"),
                    "TravelCode":result["MatchedObjectDescriptor"]["UserArea"]["Details"]["TravelCode"],
                    "ApplyOnlineUrl":result["MatchedObjectDescriptor"]["UserArea"]["Details"].get("ApplyOnlineUrl"),
                    "DetailStatusUrl":result["MatchedObjectDescriptor"]["UserArea"]["Details"].get("DetailStatusUrl"),
                    "BenefitsUrl":result["MatchedObjectDescriptor"]["UserArea"]["Details"].get("BenefitsUrl"),
                    "WithinArea":result["MatchedObjectDescriptor"]["UserArea"]["Details"]["WithinArea"],
                    "CommuteDistance":result["MatchedObjectDescriptor"]["UserArea"]["Details"]["CommuteDistance"],
                    "AgencyContactEmail":result["MatchedObjectDescriptor"]["UserArea"]["Details"].get("AgencyContactEmail"),
                    "SecurityClearance":result["MatchedObjectDescriptor"]["UserArea"]["Details"]["SecurityClearance"],
                    "DrugTestRequired":result["MatchedObjectDescriptor"]["UserArea"]["Details"]["DrugTestRequired"],
                    "RemoteIndicator":result["MatchedObjectDescriptor"]["UserArea"]["Details"]["RemoteIndicator"],
                    "load_date":datetime.now()
                    }

                parsed_user_area_data.append(user_area_data)

    except Exception as e:
        logger.error(f"An error occurred during parsing: {e}")
        return 

    try:
        db = DBUtils(logger, Config.get_db_config())

        create_query = '''
                        create schema if not exists src;

                        GRANT ALL PRIVILEGES ON SCHEMA src TO PUBLIC;
                        '''
        logger.info("Creating schema objects if not present")
        db.execute_queries(create_query)

        logger.info(f'Loading data into tables')
        db.dataframe_to_tables({"job_postings":pd.DataFrame(parsed_jobs_data), "user_area":pd.DataFrame(parsed_user_area_data)}, 'src')

        logger.info(f'Load completed')
    
    except Exception as e:
        logger.error(f"An error occurred while loading data into tables: {e}")
        return 

if __name__ == '__main__':
    file_path = extract()
    src_load(file_path)