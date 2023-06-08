from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta

def allArgsPresent(obj: object, args: list[str]) -> bool:
    """ 
        this method should be reassigned from the __init__.py of the models package
    """
    raise NotImplementedError("this shouldnt happen")

@dataclass
class CategoryRedux:
    id: str
    name: str
    total_items_in_this_category: int = 0
    
    @staticmethod
    def create(**kwargs):
        """ 
            Use this method when creating a CategoryRedux from an api response
        """
        kwargs["total_items_in_this_category"] = kwargs.get("total_items_in_this_category", 0)
        assert allArgsPresent(CategoryRedux, kwargs), "Invalid arguments for CategoryRedux"
        
        return CategoryRedux(**kwargs)
    
    @staticmethod
    def recreate(**kwargs):
        """ 
            Use this method when loading a CategoryRedux from a json file or a database record
        """
        assert allArgsPresent(CategoryRedux, kwargs), "Invalid arguments for CategoryRedux"
        
        return CategoryRedux(**kwargs)
    
    def toDict(self) -> dict:
        return asdict(self)
    
@dataclass
class CategoryData:
    category_id: str
    name: str
    picture: str
    permalink: str
    total_items_in_this_category: int
    path_from_root: list[CategoryRedux] = field(default_factory=list)
    children_categories: list[CategoryRedux] = field(default_factory=list)
    
    @staticmethod
    def create(**kwargs):
        """ 
            Use this method when creating a CategoryData from an api response
        """
        if "id" in kwargs and "category_id" not in kwargs:
            kwargs["category_id"] = kwargs["id"]
            del kwargs["id"]
        kwargs["path_from_root"] = [CategoryRedux.create(**category) for category in kwargs.get("path_from_root", [])]
        kwargs["children_categories"] = [CategoryRedux.create(**category) for category in kwargs.get("children_categories", [])]
        assert allArgsPresent(CategoryData, kwargs), "Invalid arguments for CategoryData"
        
        return CategoryData(category_id=kwargs["category_id"], name=kwargs["name"], picture=kwargs["picture"], permalink=kwargs["permalink"], total_items_in_this_category=kwargs["total_items_in_this_category"], path_from_root=kwargs["path_from_root"], children_categories=kwargs["children_categories"])
    
    @staticmethod
    def recreate(**kwargs):
        """ 
            Use this method when loading a CategoryData from a json file or a database record
        """
        kwargs["path_from_root"] = [CategoryRedux.recreate(**category) for category in kwargs.get("path_from_root", [])]
        kwargs["children_categories"] = [CategoryRedux.recreate(**category) for category in kwargs.get("children_categories", [])]
        assert allArgsPresent(CategoryData, kwargs), "Invalid arguments for CategoryData"
        
        return CategoryData(**kwargs)
    
    def toDict(self) -> dict:
        return asdict(self)
    
@dataclass
class Trend:
    keyword: str
    url: str 
    
    @staticmethod
    def create(**kwargs):
        """ 
            Use this method when creating a Trend from an api response
        """
        assert allArgsPresent(Trend, kwargs), "Invalid arguments for Trend"
        
        return Trend(**kwargs)
    
    @staticmethod
    def recreate(**kwargs):
        """ 
            Use this method when loading a Trend from a json file or a database record
        """
        assert allArgsPresent(Trend, kwargs), "Invalid arguments for Trend"
        
        return Trend(**kwargs)
    
    def toDict(self) -> dict:
        return asdict(self)
    
@dataclass
class CategoryTrends:
    category: CategoryData
    trends: list[Trend] = field(default_factory=list)
    recorded_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    @staticmethod
    def create(**kwargs):
        """ 
            dont use this method, first create the category data, the trends list and instantiate as a regular dataclass
        """
        raise NotImplementedError("you shouldn't be using create for CategoryTrends")
    
    @staticmethod
    def recreate(**kwargs):
        """ 
            Dont use this method, first create the category data, the trends list and instantiate as a regular dataclass
        """
        raise NotImplementedError("you shouldn't be using recreate for CategoryTrends")
        
    def toDict(self) -> dict:
        dict_data = {
            "category": self.category.toDict(),
            "trends": [trend.toDict() for trend in self.trends],
            "recorded_at": self.recorded_at
        }
        return dict_data