from typing import Any
from models import Seller, SellerReputation


seller_repository_interface = [
    "insert",
    "getSellerById",
    "getSellerReputationById",
    "deleteSellerById",
    "insertSellerReputation",
]


def checkMethodImplemented(cls: Any, method_name: str) -> bool:
    # hoisted function, definition should be in the __init__.py file
    raise NotImplementedError("This function wasnt defined")

class SellerRepoMeta(type):
    """
        Defines behavioral contract of the Seller Repository. Dont use directly
    """
    
    def __instancecheck__(cls, __instance: Any) -> bool:
        return cls.__subclasscheck__(type(__instance))
    
    def __subclasscheck__(cls, __subclass: type) -> bool:
        return all(checkMethodImplemented(cls, method_name) for method_name in seller_repository_interface)
    
class SellerRepository(metaclass=SellerRepoMeta):
    """
        Defines behavioral contract of the Seller Repository. Dont use directly
    """
    
    def insert(self, seller: Seller, reputation: SellerReputation) -> Exception:
        raise NotImplementedError("This method wasnt implemented")
    
    def getSellerById(self, seller_id: int) -> tuple[Seller, Exception]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getSellerReputationById(self, seller_id: int) -> tuple[SellerReputation, Exception]:
        raise NotImplementedError("This method wasnt implemented")
    
    def deleteSellerById(self, seller_id: int) -> Exception:
        raise NotImplementedError("This method wasnt implemented")
    
    def insertSellerReputation(self, reputation: SellerReputation) -> Exception:
        raise NotImplementedError("This method wasnt implemented")
    
implementation: SellerRepository = None

def setRepository(repo: SellerRepository) -> None:
    global implementation
    assert isinstance(repo, SellerRepository)
    implementation = repo
    

def insert(seller: Seller, reputation: SellerReputation) -> Exception:
    return implementation.insert(seller, reputation)

def getSellerById(seller_id: int) -> tuple[Seller, Exception]:
    return implementation.getSellerById(seller_id)

def getSellerReputationById(seller_id: int) -> tuple[SellerReputation, Exception]:
    return implementation.getSellerReputationById(seller_id)

def deleteSellerById(seller_id: int) -> Exception:
    return implementation.deleteSellerById(seller_id)

def insertSellerReputation(reputation: SellerReputation) -> Exception:
    return implementation.insertSellerReputation(reputation)
