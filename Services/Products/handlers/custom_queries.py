from flask import Blueprint, request, make_response, current_app, jsonify
from middleware.auth import token_required
import Config as service_config
import repository
import workflows
import models

custom_queries_blueprint = Blueprint('custom_queries', __name__)

@custom_queries_blueprint.route('/product', methods=['GET'])
def getCustomQuerysBySku():
    sku: str = request.args.get('sku', '')
    if not sku:
        return make_response("No sku provided", 400)
    
    custom_queries = repository.custom_querys.getCustomQuerysBySku(sku)
    
    json_queries = [query.toDict() for query in custom_queries]
    return jsonify(json_queries)

@custom_queries_blueprint.route('/', methods=['POST'])
@token_required
def createCustomQuery(user_data: dict[str, str]):
    err: Exception = None
    keyword: str = request.json.get('keyword', '')
    sku: str = request.json.get('sku', '')
    meli_id: str = request.json.get('meli_id', '')
    if not keyword and not sku and not meli_id:
        print(f"No keyword, sku or meli_id provided\n{keyword=}\n{sku=}\n{meli_id=}")
        return make_response("No keyword, sku or meli_id provided", 400)
    
    custom_query: models.CustomQuery = models.CustomQuery(keyword=keyword, sku=sku, meli_id=meli_id)
    err = repository.custom_querys.insert(custom_query)
    if err:
        print(f"Error inserting custom query: {err}")
        return make_response("Server error, sorry for the inconvinience", 500)
    
    # Emit domain event
    creator: str =user_data.get('username', 'unkown-user')
    workflows.notifiers.emitCreatedCustomQuery(creator, f"'{creator}' created a new custom query '{custom_query.keyword}' for '{custom_query.sku}'")
    
    return make_response("Custom query created", 201)

@custom_queries_blueprint.route('/', methods=['DELETE'])
@token_required
def deleteCustomQuery(user_data: dict[str, str]):
    err: Exception = None
    keyword: str = request.json.get('keyword', '')
    sku: str = request.json.get('sku', '')
    if not keyword or not sku:
        print(f"No keyword or sku provided\n{keyword=}\n{sku=}")
        return make_response("No keyword or sku provided", 400)
    
    err = repository.custom_querys.deleteCustomQuery(sku, keyword)
    if err:
        print(f"Error deleting custom query: {err}")
        return make_response("Server error, sorry for the inconvinience", 500)
    
    # Emit domain event
    creator: str =user_data.get('username', 'unkown-user')
    workflows.notifiers.emitDeletedCustomQuery(creator, f"'{creator}' deleted a custom query '{keyword}' for '{sku}'")
    
    return jsonify({"message": "Custom query deleted"})