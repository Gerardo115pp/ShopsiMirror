from typing import List, Dict
import Config as upr_config
import requests


def getSession() -> requests.Session:
    # create a requests session to reuse the same connection
    session = requests.Session()
    session.headers.update(upr_config.MELI_API_HEADERS)
    return session


    
    
    