from typing import Any

redis_cache_interface = [
    "getSearchResults",
    "getItemData",
    "setSearchResults",
    "setItemData",
]

def checkMethodImplemented(cls: Any, method_name: str) -> bool:
    # hoisted function, definition should be in the __init__.py file
    raise NotImplementedError("This function wasnt defined")

class RedisCacheMeta(type):
    """
        Defines behavioral contract of the Redis Cache. Dont use directly
    """
    
    def __instancecheck__(cls, __instance: Any) -> bool:
        return cls.__subclasscheck__(type(__instance))
    
    def __subclasscheck__(cls, __subclass: type) -> bool:
        return all(checkMethodImplemented(cls, method_name) for method_name in redis_cache_interface)

class RedisCache(metaclass=RedisCacheMeta):
    """
        Defines behavioral contract of the Redis Cache. Dont use directly
    """
    
    def getSearchResults(self, query: str) -> tuple[list, Exception]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getItemData(self, item_id: int) -> tuple[dict, Exception]:
        raise NotImplementedError("This method wasnt implemented")
    
    def setSearchResults(self, query: str, results: list, ex_minutes: int) -> Exception:
        raise NotImplementedError("This method wasnt implemented")
    
    def setItemData(self, item_id: int, data: str, ex_minutes: int) -> Exception:
        raise NotImplementedError("This method wasnt implemented")
    
implementation: RedisCache = None

def setCache(cache: RedisCache) -> None:
    global implementation
    assert isinstance(cache, RedisCache)
    implementation = cache
    
def getSearchResults(query: str) -> tuple[list, Exception]:
    return implementation.getSearchResults(query)

def getItemData(item_id: int) -> tuple[dict, Exception]:
    return implementation.getItemData(item_id)

def setSearchResults(query: str, results: list, ex_minutes: int=60) -> Exception:
    return implementation.setSearchResults(query, results, ex_minutes)

def setItemData(item_id: int, data: str, ex_minutes: int=60) -> Exception:
    return implementation.setItemData(item_id, data, ex_minutes)

