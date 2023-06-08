from typing import List, Dict, Any
from models import Product

products_repository_interface = [
    "updateStatus",
    "getActiveProducts",
    "getAllProducts", 
    "getProductById",
    "getActiveProduct"
]

def checkMethodImplemented(cls: Any, method_name: str) -> bool:
    # hoisted function, definition should be in the __init__.py file
    raise NotImplementedError("This function wasnt defined")

class ProductsRepoMeta(type):
    """
        Defines behavioral contract of the Products Repository. Dont use directly
    """
    
    def __instancecheck__(cls, __instance: Any) -> bool:
        return cls.__subclasscheck__(type(__instance))
    
    def __subclasscheck__(cls, __subclass: type) -> bool:
        # return (hasattr(__subclass, "performanceRecordExists") and callable(getattr(__subclass, "performanceRecordExists"))
        return all(checkMethodImplemented(cls, method_name) for method_name in products_repository_interface)
    
    
class ProductsRepository(metaclass=ProductsRepoMeta):
    """
        Defines behavioral contract of the Products Repository. Dont use directly
    """
    
    def updateStatus(self, product: Product, status: str) -> None:
        raise NotImplementedError("This method wasn't implemented")
    
    def getActiveProducts(self) -> List[Product]:
        raise NotImplementedError("This method wasn't implemented")
    
    def getAllProducts(self) -> List[Product]:
        raise NotImplementedError("This method wasn't implemented")
    
    def getProductById(self, product_id: int) -> Product:
        raise NotImplementedError("This method wasn't implemented")
    
    def getActiveProduct(self) -> Product:
        raise NotImplementedError("This method wasn't implemented")
    
implementation: ProductsRepository = None

def setRepository(repo: ProductsRepository) -> None:
    global implementation
    assert isinstance(repo, ProductsRepository), f"repo must be a ProductsRepository, not {type(repo)}"
    implementation = repo
    
def updateStatus(product: Product, status: str) -> None:
    implementation.updateStatus(product, status)

def getActiveProducts() -> List[Product]:
    return implementation.getActiveProducts()

def getAllProducts() -> List[Product]:
    return implementation.getAllProducts()

def getProductById(product_id: int) -> Product:
    return implementation.getProductById(product_id)

def getActiveProduct() -> Product:
    return implementation.getActiveProduct()