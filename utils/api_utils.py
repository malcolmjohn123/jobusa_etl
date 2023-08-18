import requests
import time
from typing import Dict

def get_api_data(url: str, headers: Dict, params: Dict, logger):
    """
    Fetch data from an API using the provided URL, headers, and query parameters.
    
    Args:
        url (str): The URL of the API to request data from.
        headers (dict): Headers to be included in the API request.
        params (dict): Query parameters to be included in the API request.
        logger: The logger object to record log messages.

    Returns:
        dict or None: A dictionary containing the JSON response data if the request is successful,
                      otherwise None.

    Notes:
        This function attempts to fetch data from the API using the provided URL, headers, and parameters.
        It makes up to three attempts, handling certain exceptions, and logging relevant information.

        - If a `ChunkedEncodingError` occurs during the request, the function waits for 1 second before retrying.
        - If a general `RequestException` occurs, it is logged, and None is returned.
        - If any other unexpected exception occurs, it is logged, and None is returned.
    """
    for attempt in range(3):
        try:
            logger.info(f"Sending request attempt: {attempt + 1}")
            response = requests.get(url, headers=headers, params=params)
            logger.info(f"Status: {response}")
            
            return response.json()

        except requests.exceptions.ChunkedEncodingError:
            logger.warning("ChunkedEncodingError occurred. Retrying in 1 second.")
            time.sleep(1)
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error while fetching API data: {e}")
            return None

        except Exception as e:
            logger.exception("An error occurred while fetching API data:")
            return None

    logger.error("Failed to fetch API data after 3 attempts.")
    return None
