from . import MeliAPIRequests as meli_api
from . import abstractions
from . import scrappers
import requests

Session = requests.Session # for type hinting in other modules that import this one and not requests

def getSession(custom_headers: dict) -> requests.Session:
    # create a requests session to reuse the same connection
    session = requests.Session()
    session.headers.update(custom_headers)
    return session





