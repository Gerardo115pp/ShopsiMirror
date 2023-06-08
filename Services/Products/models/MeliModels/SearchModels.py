from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from inspect import get_annotations
import json


def allArgsPresent(obj: object, args: list[str]) -> bool:
    """ 
        this method should be reassigned from the __init__.py file
    """
    raise NotImplementedError("this shouldnt happen")


@dataclass
class MeliItem:
    id: str
    name:str
    price: float
    condition: str
    original_price: float
    available_quantity: int
    free_shipping: bool
    location: str
    status: str
    url: str = field(repr=False)
    thumbnail: str = field(repr=False)
    sold_quantity: int = 0
    attributes: list[dict] = field(repr=False, default_factory=list)
    seller_id: int = 0
    
    @staticmethod
    def recreate(**kwargs) -> 'MeliItem':
        assert allArgsPresent(MeliItem, kwargs), f"not all args are present: {kwargs}"
        
        return MeliItem(**kwargs)
    
    @staticmethod
    def create(item_data: dict) -> 'MeliItem':
        id = item_data.get("id", "NO_ID" )
        name = item_data.get("title", "NO_NAME")
        price = item_data.get("price", -404)
        condition = item_data.get("condition", "NO_CONDITION")
        thumbnail = item_data.get("thumbnail", "NO_THUMBNAIL")
        original_price = item_data.get("original_price", -404)
        available_quantity = item_data.get("available_quantity", -404)
        url = item_data.get("permalink", "NO_URL")
        free_shipping = item_data.get("shipping", {}).get("free_shipping", "NO_FREE_SHIPPING")
        sold_quantity = item_data.get("sold_quantity", 0)
        status = item_data.get("status", "NO_STATUS")
        seller = item_data.get("seller", {"id": "NO_SELLER"})["id"]
        
        location = "NO_LOCATION"
        
        if "address" in item_data and item_data.get("address", {"state_name": False})["state_name"]:
            location = f"{item_data['address']['state_name']}, {item_data['address']['city_name']}"

        attributes = item_data.get("attributes", [])
        
        return MeliItem(id, name, price, condition, original_price, available_quantity, free_shipping, location, status, url, thumbnail, sold_quantity, attributes, seller)
    
    @classmethod
    def fromDict(cls, item_dict: dict) -> "MeliItem":
        # The previous definition is now on cls.create, keeping the old name for compatibility
        return cls.create(item_dict)
    
    @classmethod
    def getAttributes(cls) -> list[str]:
        return [attr for attr in get_annotations(cls).keys() if not attr.startswith("__")] 
    
    def toDict(self) -> dict:
        self_dict = asdict(self)
        self_dict["attributes"] = self.AttributeString 
        return self_dict
    
    def toJson(self) -> dict:
        """ Returns a json compatible dict with the data of the object """
        return json.dumps(self.toDict())
    
    @property
    def AttributeString(self) -> str:
        attribute_string = ""
        for attribute in self.attributes:
            attribute_string += f"{attribute['id']}: {attribute['value_name']}, "
    
        attribute_string = attribute_string[:-2] if attribute_string else "NO_ATTRIBUTES"
        return attribute_string  
    
    @property
    def Values(self) -> list[str]:
        return [
            self.id, 
            self.name, 
            self.price, 
            self.condition, 
            self.original_price, 
            self.available_quantity, 
            "Si" if self.free_shipping else "No", 
            self.location, 
            self.url, 
            self.thumbnail,
            self.AttributeString
        ]
      
    def __str__(self) -> str:
        return f"{self.name} - {self.price}"
    
    def toSql(self) -> str:
        sql_string = f"""
        (id, name, price, condition, original_price, available_quantity, free_shipping, location, url, thumbnail, attributes)
        VALUES ('{self.id}', '{self.name}', {self.price}, '{self.condition}', {self.original_price}, {self.available_quantity}, '{self.free_shipping}', '{self.location}', '{self.url}', '{self.thumbnail}', '{self.attributes}')
        """
        return sql_string.replace("\n", "")

class MeliSearchResults:
    EMPTY_QUERY = "EMPTY_QUERY"
    
    def __init__(self, items_data:dict, ttl:int=3600):
        self.__paging_data = items_data.get("paging", {
            "total": 0, # if this is bigger the 1000 the property getter will clamp it to 1000
            "primary_results": 0,
            "offset": 0,
        })
        self.__query = items_data.get("query", MeliSearchResults.EMPTY_QUERY)
        self.__ttl = datetime.now() + timedelta(seconds=ttl)
        self.__results = self._parseResults(items_data.get("results", []))
        
    def __len__(self):
        return len(self.__results)
    
    def __getitem__(self, index) -> MeliItem:
        return self.__results[index]
    
    def __iadd__(self, more_results:"MeliSearchResults") -> "MeliSearchResults":
        if isinstance(more_results, MeliSearchResults):
            assert self.__query == more_results.Query, "Cannot add results from different queries"
            
            if more_results.Offset > self.Offset:
                self.__results += more_results.Results
                self.__paging_data['offset'] = more_results.Offset
        else:
            print("Cannot add results from different type")

        return self
    
    def __iter__(self):
        return iter(self.__results)

    @property
    def isValid(self) -> bool:
        """ 
            checks if the ttl of the search cache hasnt expired
        """
        return datetime.now() < self.__ttl

    @property
    def isCompleted(self):
        """ 
            returns true if len(results) == total
        """
        return len(self.__results) <= self.__paging_data["total"]
        
    @property
    def Offset(self) -> int:
        return self.__paging_data.get("offset", 0)
    
    @property
    def Total(self) -> int:
        clamped_total = min(self.__paging_data.get("total", 0), 1000)
        return clamped_total
    
    @property
    def Results(self) -> list[MeliItem]:
        return self.__results
    
    @property
    def Dict(self) -> dict:
        dict_results = [r.toDict() for r in self.__results]
        dict_data = {
            "results": dict_results,
            "offset": self.Offset,
            "total": self.Total
        }
        
        return dict_data
    
    @property
    def Json(self) -> str:
        json_data = self.Dict
        return json.dumps(json_data)
    
    @property
    def Query(self) -> str:
        return self.__query
    
    
    def _parseResults(self, items_data:list) -> list[MeliItem]:
        return [MeliItem.create(item_data) for item_data in items_data]
