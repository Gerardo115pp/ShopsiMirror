from dataclasses import dataclass, asdict
from typing import List, Dict
import json

def allArgsPresent(obj: object, args: List[str]) -> bool:
    """ 
        this method should be reassigned from the __init__.py file
    """
    raise NotImplementedError("this shouldnt happen")


@dataclass
class Product:
    """
    Product is a dataclass that represents a product. It is used to store the data of a product in the database.
    
    
    Attributes:
        meli_id (str): the meli_id of the product
        
        name (str): the name of the product
        
        site_id (str): the site_id of the product. e.g: for mexico its 'MLM'
        
        category_id (str): the category_id of the product  
        
        initial_price (int): the initial price of the product. this is the price that the product had when it was first added to the database. for the current price, use its latest PR.
        
        secure_thumbnail (str): the secure_thumbnail's url of the product, provided by the MercadoLibre.
        
        condition (str): the condition of the product. e.g: new, used, etc.
        
        sku (str): the sku of the product. this is the internal identifier of the product used by the user. not use by MercadoLibre. Products that are not owned by the user or compete with a user product have this field empty and are called 'tracked products'.
        
        status (str): the status of the product. e.g: active, paused, etc. products that have status other than active are not considered for the performance reports.
        
        competes_with (str): if the product is owned by the user this field is empty. otherwise it's the sku of a product owned by the user that competes with this product.
        
        meli_url (str): the permalink(to be confirmed) of the product publication. 
        
        domain_id (str): the domain_id of the product. e.g: for mexico its 'MLM-CELLPHONES'
        
        seller_id (str): the seller_id of the product. this is the id of the user that owns the product publication.
        
        product_id (str): the product_id of the product. this is the id of product in the database.
        
        type (str): the type of the product. can have one of three values ['user', 'tracked', 'competitor']
        
    """
    
    meli_id: str
    name: str
    site_id: str
    category_id: str
    initial_price: int
    secure_thumbnail: str
    condition: str
    sku: str
    status: str
    competes_with: str # points to another product, if competes_with="", means its one of the customers products, if its not empty, means its a competitor and the value is the sku of a customer product
    meli_url: str
    domain_id: str
    seller_id: str
    product_id: str
    type: str
    
    @staticmethod
    def recreate(**kwargs) -> "Product":
        assert allArgsPresent(Product, kwargs), f"not all args are present: {kwargs}"
        
        return Product(**kwargs)
    
    @staticmethod
    def create(product_data: Dict) -> "Product":
        return Product.recreate(**product_data)