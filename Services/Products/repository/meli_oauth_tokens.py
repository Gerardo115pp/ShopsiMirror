from typing import Any
from models import MeliAuth

seller_repository_interface = [
    "insert",
    "getTokenByUserId",
]


def checkMethodImplemented(cls: Any, method_name: str) -> bool:
    # hoisted function, definition should be in the __init__.py file
    raise NotImplementedError("This function wasnt defined")

class MeliOauthTokens(type):
    """
        Defines behavioral contract of the Seller Repository. Dont use directly
    """
    
    def __instancecheck__(cls, __instance: Any) -> bool:
        return cls.__subclasscheck__(type(__instance))
    
    def __subclasscheck__(cls, __subclass: type) -> bool:
        return all(checkMethodImplemented(cls, method_name) for method_name in seller_repository_interface)
    
class MeliOauthRepo(metaclass=MeliOauthTokens):
    """
        Defines behavioral contract of the Seller Repository. Dont use directly
    """
    
    def insert(self, oauth_token: MeliAuth) -> Exception:
        raise NotImplementedError("This method wasnt implemented")
    
    def getTokenByUserId(self, user_id: str) -> tuple[MeliAuth, Exception]:
        raise NotImplementedError("This method wasnt implemented")
    
implementation: MeliOauthRepo = None

def setRepository(repo: MeliOauthRepo) -> None:
    global implementation
    assert isinstance(repo, MeliOauthRepo)
    implementation = repo
    
def insert(oauth_token: MeliAuth) -> Exception:
    return implementation.insert(oauth_token)

def getTokenByUserId(user_id: str) -> tuple[MeliAuth, Exception]:
    return implementation.getTokenByUserId(user_id)

