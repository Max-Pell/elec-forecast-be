import time
import requests


def get_with_retry(url:str, params:dict, max_retry=3, initial_wait=3):
    """
    Call the API with retry
    """
    try_index = 1

    while True:
        try:
            response = requests.get(url=url, params=params, timeout=30)
            response.raise_for_status()
            return response
        except requests.RequestException:
            if try_index < max_retry:
                time.sleep(initial_wait * 2 ** (try_index-1))
            else:
                raise
            try_index +=1
            


    
    