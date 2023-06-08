from bs4 import BeautifulSoup as bs
from .exceptions import MeliApiError, ScrapperError
import requests, lxml
import re


def getProductSales(meli_url: str, session: requests.Session=None, sales_extractor:re.Pattern=re.compile(r'[\d,\.]+')) -> tuple[int, Exception]:
    response: requests.Response = None
    if session:
        response = session.get(meli_url)
    else:
        response = requests.get(meli_url)
    
    if response.status_code <= 200 and response.status_code > 300:
        return 0, MeliApiError(f"Error: {response.status_code} - {response.reason}", response.status_code)
    
    html_data = bs(response.text, 'lxml')
    selector = '.ui-pdp-subtitle'
    span_container = html_data.select_one(selector)
    if not span_container:
        return 0, ScrapperError(f"Error: no span_container, {meli_url} with selector {selector}")
    
    raw_data = span_container.text
    match_data = sales_extractor.search(raw_data)
    sales = 0
    if match_data:
        sales = int(match_data.group(0).replace(',', ''))
    else:
        return 0, ScrapperError(f"Error: no sales found in {meli_url} with selector {selector}")
        
    return sales, None

def getMeliIDFromUrl(meli_url: str, session: requests.Session=None, id_extractor:re.Pattern=re.compile(r'[A-z]{2,3}-?\d{6,14}')) -> tuple[str, Exception]:
    response: requests.Response = None
    if session:
        response = session.get(meli_url)
    else:
        response = requests.get(meli_url)
    
    if response.status_code <= 200 and response.status_code > 300:
        return 0, MeliApiError(f"Error: {response.status_code} - {response.reason}", response.status_code)
    
    html_data = bs(response.text, 'lxml')
    selector = 'head meta[name="al:android:url"]'
    id_meta_tag = html_data.select_one(selector)
    if not id_meta_tag:
        return 0, ScrapperError(f"Error: no container, {meli_url} with selector {selector}")
    
    raw_data = id_meta_tag['content']
    match_data = id_extractor.search(raw_data)
    meli_id = 0
    if match_data:
        meli_id = match_data.group(0)
    else:
        return 0, ScrapperError(f"Error: no meli_id found in {meli_url} with selector {selector}")
        
    return meli_id, None