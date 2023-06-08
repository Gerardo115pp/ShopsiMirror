import HttpMessages as http_messages
import Config as service_config
from . import exceptions as workflow_exceptions
from flask_sock import Server
import repository
import models

def getCategoryData(category_id: str, oauth_token: models.MeliAuth) -> tuple[models.CategoryData, Exception]:
    category_data: models.CategoryData = None
    err: Exception = None
    
    category_data, err = http_messages.meli_api.getMeliCategoryData(category_id, oauth_token)
    if err:
        print(f"Error getting category data: {err}")
    
    return category_data, err

def getCategoryTrends(category_id: str, oauth_token: models.MeliAuth) -> tuple[list[models.Trend], Exception]:
    trends: list[models.Trend] = []
    err: Exception = None
    
    trends, err = http_messages.meli_api.getMeliCategoryTrends(category_id, oauth_token)
    if err:
        print(f"Error getting trends for category {category_id}: {err}")
    
    return trends, err

def updateProductStatus(product_data: list[models.Product]) -> Exception:
    active_products_count = len(product_data)
    products_changed = 0
    err: Exception = None
    
    for product in product_data:
        
        print(f"{product.meli_id} - {product.status}", end=": ")
        
        json_data, err = http_messages.meli_api.getMeliItemData(product.meli_id)
        if err:
            print(f"Error getting product data: {err}")
            products_changed += 1
            print(f"Product {product.meli_id} does not exists")
            repository.products.updateStatus(product, "not_found")
            continue
        
        meli_item: models.MeliItem = models.MeliItem.create(json_data)
        
        
        if meli_item.status != product.status:
            products_changed += 1
            print(f"Product {product.meli_id} status is {meli_item.status}, updating")
            repository.products.updateStatus(product, meli_item.status)
    
    print(f"{products_changed} of {active_products_count} products were updated")
    
def getApiProductData(performance_data: models.IncompletePerformanceRecord, session: http_messages.Session=None) -> tuple[models.IncompletePerformanceRecord, Exception, http_messages.Session]:
    if session == None:
        session = http_messages.getSession(service_config.MELI_API_HEADERS)
        
    product_json, err = http_messages.meli_api.getMeliItemData(performance_data.meli_id)
    if err:
        return performance_data, err, session
    
    if product_json['status'] != 'active':
        product:models.Product = repository.products.getProductById(performance_data.product_id)
        repository.products.updateStatus(product, product_json['status'])
        return None, workflow_exceptions.ProductNotFoundError(f"product {performance_data.meli_id} is not active"), session
    
    performance_data.current_price = product_json['price']
    performance_data.stock = product_json['available_quantity']
    performance_data.has_discounts = bool(product_json['original_price'])
    
    
    return performance_data, None, session

def getSalesData(performance_data: models.IncompletePerformanceRecord, session: http_messages.Session=None) -> tuple[models.IncompletePerformanceRecord, Exception, http_messages.Session]:
    if session == None:
        session = http_messages.getSession(service_config.MELI_API_HEADERS)
        
    sales, err = http_messages.scrappers.getProductSales(performance_data.meli_url, session)
    if err:
        return performance_data, err, session
    
    performance_data.sales = sales
    
    return performance_data, None, session
    
def getMeliIdFromUrl(meli_url: str, session: http_messages.Session=None) -> tuple[str, Exception]:
        
    meli_id, err = http_messages.scrappers.getMeliIDFromUrl(meli_url, session)
    if err:
        return None, err
    
    return meli_id, None