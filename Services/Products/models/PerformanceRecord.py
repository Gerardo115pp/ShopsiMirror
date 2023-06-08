from dataclasses import dataclass, asdict
from typing import List, Dict
import json

def allArgsPresent(obj: object, args: List[str]) -> bool:
    """ 
        this method should be reassigned from the __init__.py file
    """
    raise NotImplementedError("this shouldnt happen")


@dataclass
class PerformanceRecord:
    id: int
    product_id: int # this is the 'measures' attribute in the product_performance_records table, its a fk that points to the product measured.
    visits: int
    sales: int
    stock: int
    has_discounts: bool
    current_price: float
    type: str
    recorded_date: str = ""
    is_completed: bool = False
        
    @staticmethod
    def recreate(**kwargs) -> "PerformanceRecord":
        if "measures" in kwargs:
            kwargs["product_id"] = kwargs["measures"]
            del kwargs["measures"]
        
        if "has_discount" in kwargs:
            kwargs["has_discounts"] = kwargs["has_discount"]
            del kwargs["has_discount"]
            
        if 'serial' in kwargs:
            del kwargs['serial']
        
        if 'type' not in kwargs:
            kwargs['type'] = 'undefined'
        
        kwargs["is_completed"] = bool(kwargs["is_completed"])
        
        assert allArgsPresent(PerformanceRecord, kwargs), f"not all args are present: {kwargs}"
        
        return PerformanceRecord(**kwargs)
    
    @staticmethod
    def create(pr_data: Dict) -> "PerformanceRecord":
        raise NotImplementedError("a performance record should be only recreated from a db record. such record is created by the repository using an IncompletePerformanceRecord")
        
    def toDict(self) -> dict:
        return asdict(self)
    
    def toJson(self) -> str:
        return json.dumps(self.toDict())