import Config as service_config
from models import CustomQuery
import json
from pathlib import Path
import os

class CustomQueryRepository:
    def __init__(self):
        self.queries:dict[str, list[CustomQuery]] = self._loadQueries() # {sku: CustomQuery}
        
    @property
    def QuerysFile(self):
        return os.path.join(service_config.DATA_FILES, "custom_querys/querys.json") 
        
    def _loadQueries(self) -> list[CustomQuery]:
        loaded_queries = {}
        self.__createCustomQuerysFile()
        
        with open(self.QuerysFile, 'r') as f:
            queries_data = json.load(f)
            loaded_queries = {}
            for sku, querys in queries_data.items():
                loaded_queries[sku] = [CustomQuery.recreate(**query_data) for query_data in querys]
        return loaded_queries
    
    def __createCustomQuerysFile(self, file_path:str=None):
        if not file_path:
            file_path = self.QuerysFile
        if not os.path.exists(file_path):
            os.makedirs(Path(file_path).parent, exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump({}, f)
                
    def insert(self, custom_query: CustomQuery) -> Exception:
        err:Exception = None
        if custom_query.sku not in self.queries:
            self.queries[custom_query.sku] = []
        self.queries[custom_query.sku].append(custom_query)
        self._saveQueries()
        return err
    
    def getCustomQuerys(self) -> dict[str, list[CustomQuery]]:
        return self.queries
    
    def getCustomQuerysBySku(self, sku:str) -> list[CustomQuery]:
        return self.queries.get(sku, [])
    
    def deleteCustomQuery(self, sku:str, keyword) -> Exception:
        err:Exception = None
        if sku in self.queries:
            print(f"Deleting query for sku: {sku} and keyword: {keyword}")
            self.queries[sku] = [q for q in self.queries[sku] if q.keyword != keyword]
            self._saveQueries()
        return err
        
    def _saveQueries(self):
        queries_data = {sku: [] for sku in self.queries}
        for sku, querys in self.queries.items():
            queries_data[sku] = [query.toDict() for query in querys]
        with open(self.QuerysFile, 'w') as f:
            json.dump(queries_data, f, indent=4)
            