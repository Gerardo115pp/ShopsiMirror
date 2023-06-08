
from HttpMessages.MeliRequests import GetItemData
from HttpMessages.MeliResponses import MeliItemData
from bs4 import BeautifulSoup as bs
from typing import List, Dict
import Config as upr_config
from prefect import task
import repository
import models


@task
def updateProductStatus(product_data: List[models.Product]) -> Exception:
    meli_token = upr_config.MELI_TOKEN
    active_products_count = len(product_data)
    products_changed = 0
    
    log_string = f"Updating status of {active_products_count} products\n"
    
    try:
        for product in product_data:
            
            log_string += f"{product.meli_id} - {product.status}" 
            
            meli_request = GetItemData(meli_token, product.meli_id)
            meli_item:MeliItemData = meli_request.do()
            
            if meli_item == None:
                products_changed += 1
                print(f"Product {product.meli_id} does not exists")
                repository.products.updateStatus(product, "not_found")
                continue
            
            if meli_item.status != product.status:
                products_changed += 1
                print(f"Product {product.meli_id} status is {meli_item.status}, updating")
                repository.products.updateStatus(product, meli_item.status)
    except Exception as e:
        print(f"{log_string}\n\nError: {e}")
        return e
        
    del log_string
    print(f"{products_changed} of {active_products_count} products were updated")
    
