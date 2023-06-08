import HttpMessages.MeliResponses as meli_responses
import requests
import json

class GetItemData:
    """
        Class used to get the data of a single item from the MercadoLibre API. perform the GET request
        by calling the do() method.

        Raises:
            Exception: If the response.json doesn't have the expected format, an exception is raised on the do() method.

    """
    
    @staticmethod
    def getItemAPIurl(item_id: str) -> str:
        return f'https://api.mercadolibre.com/items/{item_id}'
    
    def __init__(self, token, item_id):
        self.token = token
        self.item_id = item_id

    @property
    def Headers(self):
        return {
            'Authorization': 'Bearer ' + self.token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
    def do(self) -> meli_responses.MeliItemData:
        """
        Send the GET request to the MercadoLibre API and return the response as a MeliItemData object.
        The headers include the token passed on the constructor.    

        Raises:
            Exception: If the response.json doesn't have the expected format, an exception is raised.

        Returns:
            meli_responses.MeliItemData: The response as a MeliItemData object or None if the response status code is not 200.
        """
        
        api_url = GetItemData.getItemAPIurl(self.item_id)
        
        response = requests.get(api_url, headers=self.Headers)
        if response.status_code != 200:
            print(f"ERROR: {response.status_code} - {response.reason}")
            return None
        try:
            meli_item = meli_responses.MeliItemData.fromDict(response.json())
        except Exception as e:
            raise Exception(f"ERROR ON {api_url}\n{e}")
        return meli_item