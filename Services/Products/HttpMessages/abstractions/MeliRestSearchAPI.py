from typing import List, Dict, final
import Config as service_config
import requests, json
import models

class MeliRestSearcher:
    def __init__(self, site_id="MLM", search_limit=15):
        self.__headers = service_config.MELI_API_HEADERS
        self.__site_id = site_id
        self.__exceed_primary_results = False # this should always be false 
        self.__global_search_limit = search_limit
    
    
    def composeSearchQuery(self, query:str, offset:int, limit:int, site_id:str="MLM") -> str:
        """ 
            returns the query string to be used in the search request
        """
        clean_query = query.replace(" ", "%20")
        limit = limit if limit <= 50 else 50
        return f"https://api.mercadolibre.com/sites/{site_id}/search?q={clean_query}&offset={offset}&limit={limit}"
    
    @property
    def Search_Limit(self):
        return self.__global_search_limit
        
    @Search_Limit.setter
    def Search_Limit(self, limit:int):
        if limit > 1000:
            raise ValueError("Search limit cannot be greater than 1000")
        
        self.__global_search_limit = limit
    
    @property
    def ExceedPrimaryResults(self):
        return self.__exceed_primary_results
    
    @ExceedPrimaryResults.setter
    def ExceedPrimaryResults(self, value):
        raise NotImplementedError("This property is read-only, requests cant exceed the primary results yet.")

    def search(self, query:str, offset:int=0) -> tuple[models.MeliSearchResults, Exception]:
        search_url = self.composeSearchQuery(query, offset, self.__global_search_limit)
        response = requests.get(search_url, headers=self.__headers)
        
        # check tha response status is ok
        if response.status_code < 200 or response.status_code >= 300:
            return None, Exception(f"Http Error in search items url '{search_url}': {response.status_code}: {response.text}")
        
        search_data = response.json()
        results = models.MeliSearchResults(search_data)
        return results, None