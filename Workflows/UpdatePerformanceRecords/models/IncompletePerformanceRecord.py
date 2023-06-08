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
    """
    IncompletePerformanceRecord or an IPR is a dataclass that represents a performance record that is not complete.
    an IPR is only required to have the product_id, serial, meli_id and meli_url fields. The other fields are optional.
    once all the fields are filled, the IPR is considered complete and can be converted to a PerformanceRecord. 
    
    Attributes:
        product_id (str): the product_id of the product that this record represents
        
        serial (int): the serial of the batch that this record belongs to
        
        meli_id (str): the meli_id of the product that this record represents
        
        meli_url (str): the meli_url of the product that this record represents
        
        visits (int): the amount of visits that the product had in the last 30 days
        
        sales (int): the amount of sales that the product had in the last 30 days
        
        stock (int): the current stock of the product
        
        has_discounts (bool): whether the product has discounts or not
        
        current_price (float): the current price of the product
        
    Methods:
        recreate(**kwargs) -> IncompletePerformanceRecord: loads an already existing performance record from the data passed to it
        
        create(product_id: str, meli_id: str, meli_url: str, serial:int) -> IncompletePerformanceRecord: creates a new performance record with the data passed to it
        
        isCompleted() -> bool: returns whether the performance record is complete or not
        
        hasSalesData() -> bool: returns whether the performance record has sales data or not
        
        hasVisitsData() -> bool: returns whether the performance record has visits data or not
        
        hasApiData() -> bool: returns whether the performance record has api data or not(stock, current_price)
        
        toDict() -> dict: returns the performance record as a dict
        
        toJson() -> str: returns the performance record as a json string
        

    Returns:
        _type_: _description_
    """
    
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
        """ Fuck

        Returns:
            IncompletePerformanceRecord: loads an already existing performance record from the data passed to it
        """
        assert allArgsPresent(IncompletePerformanceRecord, kwargs), f"not all args are present: {kwargs}"
        
        return IncompletePerformanceRecord(**kwargs)
    
    @staticmethod
    def create(product_id: str, meli_id: str, meli_url: str, serial:int) -> "IncompletePerformanceRecord":
        
        return IncompletePerformanceRecord(product_id, serial, meli_id, meli_url)
    
    @property
    def isCompleted(self) -> bool:
        """
        Return true if the IPR has all measures filled in.
        """
        return self.hasVisitsData and self.hasSalesData and self.hasApiData
    
    @property
    def hasSalesData(self) -> bool:
        """
        Does the IPR has the item's sales registered?
        """
        return self.sales != -1
    
    @property
    def hasVisitsData(self) -> bool:
        """
        Does the IPR has the item's visits registered?
        """
        return self.visits != -1
    
    @property
    def hasApiData(self) -> bool:
        """
        Does the IPR has the item's stock and current_price registered? 
        """
        return self.stock != -1 and self.current_price != -1
    
    def toDict(self) -> dict:
        return asdict(self)
    
    def toJson(self) -> str:
        """
        Returns the IPR as a json string with 4 spaces of indentation.
        """
        return json.dumps(self.toDict(), indent=4)