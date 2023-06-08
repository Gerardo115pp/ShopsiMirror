from flask import Blueprint, request, make_response, current_app
from HttpMessages.MeliAPIRequests import getMeliItemData
from HttpMessages.abstractions import MeliSearchAPI
from middleware.auth import token_required
import Config as service_config
import repository
import workflows
import models
import json

items_blueprint = Blueprint('items', __name__)
search_cache:dict[str, models.MeliSearchResults] = {}

@items_blueprint.route('/search', methods=['GET'])
@token_required
def searchItems(user_data: dict[str, str]):
    query = request.args.get('query', '')
    user_limit = request.args.get('limit', "-1")
    user_limit = int(user_limit) if user_limit.isnumeric() else -1
    if not query:
        return make_response("No query provided", 406)
    
    search_engine = MeliSearchAPI(site_id="MLM",search_limit=50) # search on mexican site, limit 50 results per request
    cached_results:models.MeliSearchResults = search_cache.get(query, None) # check if the query is cached
    
    offset = 0
    limit = 50
    if cached_results and cached_results.isValid:
        print("Using cached results")
        offset = len(cached_results)
        limit = cached_results.Total
        
    if user_limit != -1 and user_limit <= limit:
        limit = user_limit
        
    print(f"Searching for {query} from {offset} to {limit}")
    
    # Emit domain event
    creator: str =user_data.get('username', 'unkown-user')
    workflows.notifiers.emitProductSearchPerformed(creator, f"{creator} searched for '{query}'")
    
    
    if offset >= limit or offset >= 1000: # 1000 is the max limit imposed by meli api
        print(f"Offset {offset} is greater than limit {limit}")
        json_results = cached_results.Dict
        json_results["owner_id"] = service_config.OWNER_ACCOUNT_ID
        return make_response(json_results, 200)
    
    new_results, error = search_engine.search(query, offset)
    if error:
        print(f"Error searching for '{query}': {error}\n{offset=}, {limit=}")
        return make_response("Server error, sorry for the inconvinience", 500)
    
    if not cached_results:
        print(f"Creating new cache for '{query}' with {len(new_results)} results")
        search_cache[query] = new_results
        cached_results = new_results
    else:
        print(f"Adding {len(new_results)} results to cache for '{query}'")
        cached_results += new_results
    
    print(f"Returning {len(cached_results)} results")
    json_results = cached_results.Dict
    json_results["owner_id"] = service_config.OWNER_ACCOUNT_ID
    return make_response(json_results, 200)
        
@items_blueprint.route('/item', methods=['GET'])
@token_required
def getMeliItemDataById(user_data: dict[str, str]):
    jwt_params = request.args.get('data', '')
    
    if not jwt_params:
        print("No id provided")
        return make_response("No id provided", 400)

    cached_response, error = repository.redis_cache.getItemData(jwt_params)
    if error == None:
        response = make_response(cached_response, 200)
        response.headers['Content-Type'] = 'application/json'
        
        return response

    parametes, error = workflows.parsers.parseJwtParameters(jwt_params)
    if error:
        print(f"Error parsing jwt parameters: {error}")
        return make_response("Invalid jwt parameters", 400)
    
    assert type(parametes) is dict
    print(f"Parameters: {parametes}")
    
    if parametes.get('item_id', None) is None or parametes.get('item_url', None) is None:
        print(f"Missing parameters meli_id or meli_url in: {parametes}")
        return make_response("No id provided", 400)
    
    item_id = parametes.get('item_id')
    item_details, error = getMeliItemData(item_id)
    if error:
        real_item_id, error = workflows.collectors.getMeliIdFromUrl(parametes.get('item_url'))
        
        if not error:
            item_details, error = getMeliItemData(real_item_id)
            
        if error:
            print(f"Error getting item details for '{item_id}': {error}")
            return make_response("Server error, sorry for the inconvinience", 500)
    
    repository.redis_cache.setItemData(jwt_params, json.dumps(item_details))
    
    response = make_response(item_details, 200)
    response.headers['Content-Type'] = 'application/json'
    
    return response
    
    
