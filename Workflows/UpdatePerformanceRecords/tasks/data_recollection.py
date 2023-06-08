from bs4 import BeautifulSoup as bs
import requests, lxml
from typing import List, Dict, Tuple
import Config as upr_config
from prefect import task
import repository
import models
import re
    
class ProductNotFoundError(Exception):
    pass

class NoSalesFoundError(Exception):
    pass

class MeliAPIError(Exception):
    pass
    
@task
def getApiProductData(performance_data: models.IncompletePerformanceRecord, session: requests.Session) -> Tuple[models.IncompletePerformanceRecord, Exception]:
    """
        Gets the current price, stock and if the product has discounts from the meli api. Also checks if the product is active and if it is not, it removes it from the incomplete_performance_records table.

        Args:
            performance_data (models.IncompletePerformanceRecord): An incomplete performance record, it should have the meli_id and product_id fields filled.
            session (requests.Session): A requests session to use for the request.

        Returns:
            Tuple[models.IncompletePerformanceRecord, Exception]: The updated performance_data and an error if there was one.
    """
    
    response = session.get(f"https://api.mercadolibre.com/items/{performance_data.meli_id}?include_attributes=all")
    if response.status_code != 200:
        return None, MeliAPIError(f"Error: {response.status_code} - {response.reason}")
    
    product_json = response.json()
        
    if product_json['status'] != 'active':
        product:models.Product = repository.products.getProductById(performance_data.product_id)
        repository.products.updateStatus(product, product_json['status'])
        repository.incomplete_performance_records.removeIPR(performance_data)
        return None, ProductNotFoundError(f"product {performance_data.meli_id} is not active")
    
    performance_data.current_price = product_json['price']
    performance_data.stock = product_json['available_quantity']
    performance_data.has_discounts = bool(product_json['original_price'])
    
    
    return performance_data, None

@task
def getSalesData(performance_data: models.IncompletePerformanceRecord, sales_extractor:re.Pattern=re.compile(r'[\d,\.]+')) -> Tuple[models.IncompletePerformanceRecord, Exception]:
    response = requests.get(performance_data.meli_url)
    
    if response.status_code != 200:
        if response.status_code == 404:
            product:models.Product = repository.products.getProductById(performance_data.product_id)
            repository.products.updateStatus(product, "not_found")
            repository.incomplete_performance_records.removeIPR(performance_data)
        return None, ProductNotFoundError(f"ERROR: {response.status_code} - {response.reason}")
    
    html_data = bs(response.text, 'lxml')
    span_container = html_data.select_one('.ui-pdp-subtitle')
    if not span_container:
        return None, NoSalesFoundError(f"Error: no span_container, {performance_data.meli_id}")
    
    raw_data = span_container.text
    match_data = sales_extractor.search(raw_data)
    sales = 0
    if match_data:
        sales = int(match_data.group(0).replace(',', ''))
        
    performance_data.sales = sales
    
    return performance_data, None

@task(retries=upr_config.VISITS_API_RETRYS, retry_delay_seconds=upr_config.AWAIT_TIME)
def getVisitsData(performance_data: models.IncompletePerformanceRecord, session: requests.Session) -> Tuple[models.IncompletePerformanceRecord, Exception]:
    response = session.get(f"https://api.mercadolibre.com/visits/items?ids={performance_data.meli_id}", headers=upr_config.MELI_API_HEADERS)
    
    # handle 429 Too Many Requests
    if response.status_code == 429:
        raise MeliAPIError(f"too many retrys - Failure while getting visits data for {performance_data.meli_id}")
    
    if response.status_code != 200:
        return None, MeliAPIError(f"Error: {response.status_code} - {response.reason}")
    
    #We only raise an exception if the API returns 429 so prefect will retry the task, any other error should not be retried.
    visits_json = response.json()
    performance_data.visits = visits_json[performance_data.meli_id]
    
    return performance_data, None


