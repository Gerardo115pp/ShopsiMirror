from .redis_utils import REDIS_CONFIG, RedisConnection
import json
from datetime import timedelta


class RedisCache:
    def __init__(self, config: REDIS_CONFIG=None):
        self.config = config or REDIS_CONFIG.createFromEnv()
        
    def getSearchResults(self, query: str) -> tuple[list, Exception]:
        json_data = []
        err = None
        
        with RedisConnection(self.config) as conn:
            data = conn.get(f"search-{query}")
            if not data:
                print("No data found")
                return json_data, Exception("No data found")

            try:
                json_data = json.loads(data)
            except Exception as e:
                err = e
                print(f"Error parsing json: {e}")
            
        return json_data, err
            
    def setSearchResults(self, query: str, data: str, ex_minutes: int) -> Exception:
        if type(data) != str:
            return Exception("Data must be a string")
        
        with RedisConnection(self.config) as conn:
            conn.set(f"search-{query}", data, ex=timedelta(minutes=ex_minutes))
            
        return None
    
    def getItemData(self, item_id: int) -> tuple[dict, Exception]:
        json_data = {}
        err = None
        
        with RedisConnection(self.config) as conn:
            data = conn.get(f"item-data-{item_id}")
            if not data:
                return json_data, Exception("No data found")

            try:
                json_data = json.loads(data)
            except Exception as e:
                err = e
                print(f"Error parsing json: {e}")
            
        return json_data, err
    
    def setItemData(self, item_id: int, data: str, ex_minutes: int) -> Exception:
        if type(data) != str:
            return Exception("Data must be a string")
        
        with RedisConnection(self.config) as conn:
            conn.set(f"item-data-{item_id}", data, ex=timedelta(minutes=ex_minutes))
            
        return None