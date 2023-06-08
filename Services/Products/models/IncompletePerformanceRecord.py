from dataclasses import dataclass, asdict
from typing import List
import json

def allArgsPresent(obj: object, args: List[str]) -> bool:
    """ 
        this method should be reassigned from the __init__.py file
    """
    raise NotImplementedError("this shouldnt happen")

@dataclass
class IncompletePerformanceRecord:
    product_id: str
    serial: int
    meli_id: str
    meli_url: str = ""
    visits: int = -1
    sales: int = -1
    stock: int = -1
    has_discounts: bool = False
    current_price: float = -1
        
    @staticmethod
    def recreate(**kwargs) -> "IncompletePerformanceRecord":
        assert allArgsPresent(IncompletePerformanceRecord, kwargs), f"not all args are present: {kwargs}"
        
        return IncompletePerformanceRecord(**kwargs)
    
    @staticmethod
    def create(product_id: str, meli_id: str, meli_url: str, serial:int) -> "IncompletePerformanceRecord":
        return IncompletePerformanceRecord(product_id, serial, meli_id, meli_url)
    
    @property
    def isCompleted(self) -> bool:
        return self.hasVisitsData and self.hasSalesData and self.hasApiData
    
    @property
    def hasSalesData(self) -> bool:
        return self.sales != -1
    
    @property
    def hasVisitsData(self) -> bool:
        return self.visits != -1
    
    @property
    def hasApiData(self) -> bool:
        return self.stock != -1 and self.current_price != -1
    
    def toDict(self) -> dict:
        return asdict(self)
    
    def toJson(self) -> str:
        return json.dumps(self.toDict(), indent=4)