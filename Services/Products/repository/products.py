from typing import List, Dict, Any
from models import Product

products_repository_interface = [
    "insert",
    "insertTrackedProduct",
    "updateStatus",
    "getActiveProducts",
    "getAllProducts", 
    "getProductById",
    "getOurProducts",
    "getCompetitorProducts",
    "getTrackedProducts",
    "getPerformanceReport",
    "getProductCompetitors"
    
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
        for method_name in products_repository_interface:
            if not checkMethodImplemented(cls, method_name):
                print(f"Method {method_name} not implemented in {__subclass}")
                return False
        return True
        # return all(checkMethodImplemented(cls, method_name) for method_name in products_repository_interface)
    
    
class ProductsRepository(metaclass=ProductsRepoMeta):
    """
        Defines behavioral contract of the Products Repository. Dont use directly
    """
    
    def insert(self, product: Product) -> Exception:
        raise NotImplementedError("This method wasnt implemented")
    
    def insertTrackedProduct(self, new_product: Product) -> Exception:
        raise NotImplementedError("This method wasnt implemented")
    
    def updateStatus(self, product: Product, status: str) -> None:
        raise NotImplementedError("This method wasnt implemented")
    
    def getActiveProducts(self) -> List[Product]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getAllProducts(self) -> List[Product]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getProductById(self, product_id: int) -> Product:
        raise NotImplementedError("This method wasnt implemented")
    
    def getOurProducts(self) -> List[Product]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getCompetitorProducts(self) -> List[Product]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getTrackedProducts(self) -> List[Product]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getPerformanceReport(self) -> List[Dict]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getProductCompetitors(self, product_id: int) -> List[Product]:
        raise NotImplementedError("This method wasnt implemented")
    
implementation: ProductsRepository = None

def setRepository(repo: ProductsRepository) -> None:
    global implementation
    assert isinstance(repo, ProductsRepository), f"repo must be a ProductsRepository, not {type(repo)}"
    implementation = repo

def insert(product: Product) -> Exception:
    return implementation.insert(product)

def updateStatus(product: Product, status: str) -> None:
    implementation.updateStatus(product, status)

def getActiveProducts() -> List[Product]:
    return implementation.getActiveProducts()

def getAllProducts() -> List[Product]:
    return implementation.getAllProducts()

def getProductById(product_id: int) -> Product:
    return implementation.getProductById(product_id)

def getOurProducts() -> List[Product]:
    return implementation.getOurProducts()

def getCompetitorProducts() -> List[Product]:
    return implementation.getCompetitorProducts()

def getTrackedProducts() -> List[Product]:
    return implementation.getTrackedProducts()

def getPerformanceReport() -> List[Dict]:
    return implementation.getPerformanceReport()

def getProductCompetitors(product_id: str) -> List[Product]:
    return implementation.getProductCompetitors(product_id)

def insertTrackedProduct(new_product: Product) -> Exception:
    return implementation.insertTrackedProduct(new_product)