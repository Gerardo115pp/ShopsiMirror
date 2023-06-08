from dataclasses import dataclass, asdict
from typing import List
import json

def allArgsPresent(obj: object, args: List[str]) -> bool:
    """ 
        this method should be reassigned from the __init__.py file
    """
    raise NotImplementedError("this shouldnt happen")


@dataclass
class PerformanceRecord:
    """
    PerformanceRecord or a PR is a dataclass that represents a performance record that is complete. A PR is a collection
    of attributes related to a single item recorded in a specific point in time which is represented by its serial.
    
    Attributes:
        id (int): the id of the record in the database
        product_id (int): the product_id of the product that this record represents. on the database, this is the 'measures' attribute
        visits (int): the amount of visits that the product had in the last 30 days
        sales (int): the amount of sales that the product had in the last 30 days
        stock (int): the current stock of the product
        has_discounts (bool): whether the product has discounts or not
        current_price (float): the current price of the product
        keyword_file (str): kept for use in the future. currently not used and not considered for anything.
        date (str): the date when this record was created. this is a generated column in the database.
        
    Methods:
        recreate(**kwargs) -> PerformanceRecord: loads an already existing performance record from the data passed to it
        create(product_id: int, visits: int, sales: int, stock: int, has_discounts: bool, current_price: float, keyword_file: str, date: str) -> PerformanceRecord: creates a new performance record with the data passed to it
        toDict() -> dict: returns the performance record as a dict
        toJson() -> str: returns the performance record as a json string
    """
    
    id: int
    product_id: int # this is the 'measures' attribute in the product_performance_records table, its a fk that points to the product measured.
    visits: int
    sales: int
    stock: int
    has_discounts: bool
    current_price: float
    keyword_file = "TODO"
    date: str = ""
        
    @staticmethod
    def recreate(**kwargs) -> "PerformanceRecord":
        if "measures" in kwargs:
            kwargs["product_id"] = kwargs["measures"]
            del kwargs["measures"]
        
        assert allArgsPresent(PerformanceRecord, kwargs), f"not all args are present: {kwargs}"
        
        return PerformanceRecord(**kwargs)
    
    @staticmethod
    def create(*args, **kwargs) -> "PerformanceRecord":
        raise NotImplementedError("a performance record should be only recreated from a db record. such record is created by the repository using an IncompletePerformanceRecord")
        
    def toDict(self) -> dict:
        return asdict(self)
    
    def toJson(self) -> str:
        return json.dumps(self.toDict())