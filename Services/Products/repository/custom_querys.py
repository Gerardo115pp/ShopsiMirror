from models import CustomQuery
from typing import Any

custom_querys_repository_interface = [
    "insert",
    "getCustomQuerys",
    "getCustomQuerysBySku",
    "deleteCustomQuery"
]

def checkMethodImplemented(cls: Any, method_name: str) -> bool:
    # hoisted function, definition should be in the __init__.py file
    raise NotImplementedError("This function wasnt defined")

class CustomQuerysRepoMeta(type):
    """
        Defines behavioral contract of the CustomQuerys Repository. Dont use directly
    """
    
    def __instancecheck__(cls, __instance: Any) -> bool:
        return cls.__subclasscheck__(type(__instance))
    
    def __subclasscheck__(cls, __subclass: type) -> bool:
        for method_name in custom_querys_repository_interface:
            if not checkMethodImplemented(cls, method_name):
                print(f"Method {method_name} not implemented in {__subclass}")
                return False
        return True
        
class CustomQuerysRepository(metaclass=CustomQuerysRepoMeta):
    """
        Defines behavioral contract of the CustomQuerys Repository. Dont use directly
    """
    
    def insert(self, custom_query: CustomQuery) -> Exception:
        raise NotImplementedError("This method wasnt implemented")
    
    def getCustomQuerys(self) -> list[CustomQuery]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getCustomQuerysBySku(self, sku: str) -> list[CustomQuery]:
        raise NotImplementedError("This method wasnt implemented")
    
    def deleteCustomQuery(self, sku: str, keyword: str) -> None:
        raise NotImplementedError("This method wasnt implemented")
    
implementation: CustomQuerysRepository = None

def setRepository(repo: CustomQuerysRepository) -> None:
    global implementation
    assert isinstance(repo, CustomQuerysRepository)
    implementation = repo
    
def insert(custom_query: CustomQuery) -> Exception:
    return implementation.insert(custom_query)

def getCustomQuerys() -> list[CustomQuery]:
    return implementation.getCustomQuerys()

def getCustomQuerysBySku(sku: str) -> list[CustomQuery]:
    return implementation.getCustomQuerysBySku(sku)

def deleteCustomQuery(sku: str, keyword: str) -> Exception:
    return implementation.deleteCustomQuery(sku, keyword)