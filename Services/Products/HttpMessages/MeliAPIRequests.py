from datetime import datetime, timedelta
from .exceptions import MeliApiError
from bs4 import BeautifulSoup as bs
import Config as service_config
import requests
import models
import lxml

assert hasattr(service_config, "MELI_API_HEADERS"), "MELI_API_HEADERS not found in Config.py"

def composeApiHeaders(meli_auth: models.MeliAuth=None) -> dict:
    headers = service_config.MELI_API_HEADERS
    if meli_auth:
    
        assert meli_auth.isValid(), "MeliAuth is not valid or has expired"
        token = meli_auth.access_token
        
        headers = {
            "Authorization": f"{meli_auth.token_type} {meli_auth.access_token}",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
    
    return headers

def getMeliItemData(meli_id:str) -> tuple[dict, Exception]:
    """ 
        returns the item data from the meli api
    """
    
    item_url = f"https://api.mercadolibre.com/items/{meli_id}"
    response = requests.get(item_url, headers=service_config.MELI_API_HEADERS)
    if response.status_code > 299 or response.status_code < 200:
        return {}, MeliApiError(f"\nError in the request: {response.status_code}, url: {item_url}", response.status_code)
    
    item_data = response.json()
    
    return item_data, None

def getMeliSeller(seller_id: int, meli_oauth: models.MeliAuth) ->tuple[models.Seller, models.SellerReputation, Exception]:
    """ 
        returns the seller data from the meli api
    """
    seller_url = f"https://api.mercadolibre.com/users/{seller_id}"
    
    oauth_headers = composeApiHeaders(meli_oauth)
    
    response = requests.get(seller_url, headers=oauth_headers)
    if response.status_code > 299 or response.status_code < 200:
        return None, None, requests.HTTPError(f"\nError in the request: {response.status_code}, url: {seller_url}")
    seller_data:dict = response.json()
    try:
        print(f"Creating seller from meli data: {seller_data}")
        seller = models.Seller.fromMeliData(seller_data)
        print(f"Creating seller reputation from meli data: {seller_data}")
        reputation = models.SellerReputation.fromMeliData(seller_data['seller_reputation'], seller.seller_id)
        print("Done")
    except Exception as e:
        print(f"Error creating seller or reputation from meli data: {e}")
        return None, None, e
    
    return seller, reputation, None

def exchangeAccessToken(meli_auth: models.MeliAuth) -> tuple[models.MeliAuth, Exception]:
    """ 
        exchanges the access code for an access token, and returns it
    """
    request_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    request_body = {
        "grant_type": meli_auth.grant_type,
        "client_id": meli_auth.client_id,
        "client_secret": meli_auth.client_secret,
        "code": meli_auth.code,
        "redirect_uri": meli_auth.redirect_uri
    }
    response = requests.post("https://api.mercadolibre.com/oauth/token", headers=request_headers, data=request_body)
    if response.status_code > 299 or response.status_code < 200:
        return None, requests.HTTPError(f"\nError in the request: {response.status_code}, url: https://api.mercadolibre.com/oauth/token\n{response.text}")
    
    try:
        response_data = response.json()
        meli_auth.access_token = response_data['access_token']
        meli_auth.token_type = response_data['token_type']
        meli_auth.Duration = response_data['expires_in']
        meli_auth.scope = response_data['scope']
        meli_auth.refresh_token = response_data['refresh_token']
    except Exception as e:
        return None, Exception(f"Error parsing response data: {e}\n response body: {response.text}\n response headers: {response.headers}\n response status code: {response.status_code}")
    
    return meli_auth, None

def refreshAccessToken(meli_auth: models.MeliAuth) -> tuple[models.MeliAuth, Exception]:
    """ 
        refreshes the access token, and returns it
    """
    request_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    request_body = {
        "grant_type": "refresh_token",
        "client_id": meli_auth.client_id,
        "client_secret": meli_auth.client_secret,
        "refresh_token": meli_auth.refresh_token
    }
    response = requests.post("https://api.mercadolibre.com/oauth/token", headers=request_headers, data=request_body)
    if response.status_code > 299 or response.status_code < 200:
        return None, requests.HTTPError(f"\nError in the request: {response.status_code}, url: https://api.mercadolibre.com/oauth/token\n{response.text}")
    
    try:
        response_data = response.json()
        meli_auth.access_token = response_data['access_token']
        meli_auth.token_type = response_data['token_type']
        meli_auth.Duration = response_data['expires_in']
        meli_auth.scope = response_data['scope']
        meli_auth.user_id = response_data['user_id']
        meli_auth.refresh_token = response_data['refresh_token']
    except Exception as e:
        return None, Exception(f"Error parsing response data: {e}\n response body: {response.text}\n response headers: {response.headers}\n response status code: {response.status_code}")
    
    return meli_auth, None

def getMeliCategoryData(category_id: str, user_token: models.MeliAuth) -> tuple[models.CategoryData, Exception]:
    """ 
        returns the category data from the meli api
    """
    category_url = f"https://api.mercadolibre.com/categories/{category_id}"
    authoritative_headers = composeApiHeaders(user_token)
    response = requests.get(category_url, headers=authoritative_headers)
    if response.status_code > 299 or response.status_code < 200:
        return None, requests.HTTPError(f"\nError in the request: {response.status_code}\n url: {category_url}\n headers: {authoritative_headers}\nmessage{response.text}")
    category_json_data:dict = response.json()
    try:
        category_data:models.CategoryData = models.CategoryData.create(**category_json_data)
    except Exception as e:
        return None, Exception(f"Error creating category data from meli data: {e}")
    
    return category_data, None

def getMeliCategoryTrends(category_id: str, user_token: models.MeliAuth, site_id:str="MLM") -> tuple[list[models.Trend], Exception]:
    """ 
        returns the category trends from the meli api
    """
    category_url = f"https://api.mercadolibre.com/trends/{site_id}/{category_id}"
    authoritative_headers = composeApiHeaders(user_token)
    
    response = requests.get(category_url, headers=authoritative_headers)
    if response.status_code > 299 or response.status_code < 200:
        return None, requests.HTTPError(f"\nError in the request: {response.status_code}\n url: {category_url}\n headers: {authoritative_headers}\nmessage{response.text}")
    
    category_json_data:list[dict] = response.json()
    
    try:
        trends:list[models.Trend] = [models.Trend.create(**trend) for trend in category_json_data]
    except Exception as e:
        return None, Exception(f"Error creating category data from meli data: {e}")
    
    return trends, None





