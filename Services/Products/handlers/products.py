from flask import Blueprint, request, make_response, jsonify, send_from_directory
from HttpMessages.MeliAPIRequests import getMeliItemData
from middleware.auth import token_required
from datetime import datetime
from typing import List, Dict
import openpyxl as excel
import repository
import Config as service_config
import models
import workflows
import os


""" 
    A Product is a representation of a product already registered on the system
"""

products_blueprint = Blueprint('products', __name__)


@products_blueprint.route('/', methods=['GET'])
@token_required
def hanldeGetProducts():
    products = repository.products.getAllProducts()
    
    response = jsonify(products)
    response.status_code = 200 if products else 404
    return response

@products_blueprint.route('/', methods=['POST'])
@token_required
def handleCreateProduct(user_data: dict[str, str]):
    
    request_data = request.get_json()
    err:Exception = None
    new_product:models.Product = None
    
    #validate request data
    if not request_data:
        response = jsonify({"message": "No data provided"})
        response.status_code = 400
        return response
    
    item_data = request_data['item_data']
    item_sku = request_data['competes_with']
    if not item_sku:
        # misdirected request
        return make_response("This is ment to create competitors, not regular products", 421)

    #Getting the necessary data to create a product
    product, err = workflows.creators.createProductFromMeliData(item_data, item_sku)
    product.competes_with = item_sku
    print(f"Creating product {product.meli_id}")
    if err:
        print(f"Error creating product: {err}")
        response = jsonify({"message": "Error getting product data from Meli", "error": str(err)})
        response.status_code = 500
        return response
    
    #check if the product already exists and status is deleted
    existing_product = repository.products.getProductById(product.product_id)
    if existing_product != None and existing_product.status == "deleted":
        repository.products.updateStatus(existing_product, product.status)
        print(f"Product {product.product_id} already exists, updating status to {product.status}")
        response = make_response()
        response.status_code = 200
        return response
    
    #verify that the seller is not the same as the OWNER_ACCOUNT_ID
    if product.seller_id == service_config.OWNER_ACCOUNT_ID:
        print(f"ERROR: trying to own a product as a competitor: {product.meli_id}")
        response = jsonify({"message": "has utilizado una ruta incorrecta para crear un producto propio"})
        response.status_code = 421
        return response
    
    #checking if the product seller is already registered on the system or if needs to be created
    seller:models.Seller = None
    seller, err = repository.sellers.getSellerById(product.seller_id)
    
    if err:
        print(f"Error getting seller: {err}")
        response = jsonify({"message": "Error getting seller data from database", "error": str(err)})
        response.status_code = 500
        return response
    
    # if seller does not exist, create it
    if seller == None:
        # new seller, create it
        
        # get the users oauth token
        meli_oauth_token: models.MeliAuth
        user_id = user_data.get('user_id', None)
        assert user_id, "user_id not found in user_data"
        
        meli_oauth_token, err = repository.meli_oauth_tokens.getTokenByUserId(user_id)
        if err:
            print(f"The requesting user has not linked his meli account: {err}")
            return make_response("User not authenticated", 403)
        
        seller_reputation:models.SellerReputation = None
        seller, seller_reputation, err = workflows.creators.createSellerFromId(product.seller_id, meli_oauth_token)
        if err:
            print(f"Error getting seller data from meli api: {err}")
            response = jsonify({"message": "Error getting seller data from Meli", "error": str(err)})
            response.status_code = 500
            return response
        
        err = repository.sellers.insert(seller, seller_reputation)
        print(f"Response from inserting seller: {err}")
        if err:
            print(f"Error inserting seller: {err}")
            response = jsonify({"message": "Error inserting seller data into database", "error": str(err)})
            response.status_code = 500
            return response
    
    err = repository.products.insert(product) # if returns !None, must likely means that the product already exists
    if err:
        print(f"Error inserting product: {err}")
        response = jsonify({"message": "Error inserting product data into database", "error": str(err)})
        response.status_code = 402 # this is probably a duplicate product error
        return response
    
    # Emit domain event
    creator: str =user_data.get('username', 'unkown-user')
    workflows.notifiers.emitProductCompetitorsUpdated(creator, f"'{creator}' added a new competitor product '{product.meli_id}' to '{product.competes_with}'")
    
    return make_response("ok", 201)

@products_blueprint.route('/track', methods=['POST'])
@token_required
def handleCreateTrackedProduct(user_data: dict[str, str]):
    request_data = request.get_json()
    err:Exception = None
    
    #validate request data
    if not request_data:
        response = jsonify({"message": "No data provided"})
        response.status_code = 400
        return response
    
    item_data = request_data.get('item_data', None)
    sku = request_data.get('sku', None)
    if item_data == None or sku == None:
        # misdirected request
        return make_response("no product data", 400)
    
    if 'title' not in item_data: #its not item data, but a catalog item data. it still have the id so we can retrieve the item data from it
        item_data, err = getMeliItemData(item_data['id'])
        if err:
            print(f"Error getting item data from meli: {err}")
            return make_response("data provided was not sufficient and it was impossible to retrieve the item data from meli", 406)
        
    #Getting the necessary data to create a product
    try:
        product = models.Product.fromItemData(item_data, sku, False)
    except Exception as e:
        print(f"Error creating product: {e}")
        return make_response("incorrect data or format, unparsable item_data", 406)
    
    
    #check if the product already exists and status is deleted
    existing_product = repository.products.getProductById(product.product_id)
    if existing_product != None and existing_product.status == "deleted":
        repository.products.updateStatus(existing_product, product.status)
        print(f"Product {product.product_id} already exists, updating status to {product.status}")
        response = make_response()
        response.status_code = 200
        return response
    
    #verify that the seller is not the same as the OWNER_ACCOUNT_ID
    if product.seller_id == service_config.OWNER_ACCOUNT_ID:
        print(f"ERROR: trying to own a product as a competitor: {product.meli_id}")
        response = jsonify({"message": "has utilizado una ruta incorrecta para crear un producto propio"})
        response.status_code = 417 # expectation failed
        return response
    
    #checking if the product seller is already registered on the system or if needs to be created
    seller:models.Seller = None
    seller, err = repository.sellers.getSellerById(product.seller_id)
    
    if err:
        print(f"Error getting seller: {err}")
        response = jsonify({"message": "Error getting seller data from database", "error": str(err)})
        response.status_code = 500
        return response
    
    # if seller does not exist, create it
    if seller == None:
        # new seller, create it
        
        # first get the user oauth token
        user_id = user_data.get('user_id', None)
        assert user_id, "user_id not found in user_data"
        
        meli_auth:models.MeliAuth = None
        
        meli_auth, err = repository.meli_oauth_tokens.getTokenByUserId(user_id)
        if err:
            return make_response("Error getting user oauth token", 403)
        
        seller_reputation:models.SellerReputation = None
        seller, seller_reputation, err = workflows.creators.createSellerFromId(product.seller_id, meli_auth)
        if err:
            print(f"Error getting seller data from meli api: {err}")
            response = jsonify({"message": "Error getting seller data from Meli", "error": str(err)})
            response.status_code = 500
            return response
        err = repository.sellers.insert(seller, seller_reputation)
        print(f"Response from inserting seller: {err}")
        if err:
            print(f"Error inserting seller: {err}")
            response = jsonify({"message": "Error inserting seller data into database", "error": str(err)})
            response.status_code = 500
            return response
        
    err = repository.products.insertTrackedProduct(product) # if returns !None, must likely means that the product already exists
    if err:
        print(f"Error inserting product: {err}")
        response = jsonify({"message": "Error inserting product data into database", "error": str(err)})
        response.status_code = 402
    
    # Emit domain event
    creator: str =user_data.get('username', 'unkown-user')
    workflows.notifiers.emitNewProductTracked(creator, f"'{creator}' added a new tracked product '{product.meli_id}' with sku '{product.sku}'")
    
    return make_response("ok", 201)
    
@products_blueprint.route('/track', methods=['GET'])
@token_required
def handleGetTrackedProducts(user_data: dict[str, str]):
    tracked_products = repository.products.getTrackedProducts()
    return jsonify(tracked_products)

@products_blueprint.route('/ours', methods=['GET'])
@token_required
def handleGetOurProducts():
    """ 
        Returns a list of all of our products with a list of their competitors.
    """
    products = repository.products.getOurProducts()
    competitors = repository.products.getCompetitorProducts()
    look_up_table:Dict[str, models.OurProduct] = {} # {our_product_sku: [ ...our_product, competitors:List]}
    for our_product in products:
        new_our_product = models.OurProduct(our_product, [])
        look_up_table[our_product.sku] = new_our_product
    for competitor in competitors:
        if competitor.sku in look_up_table:
            look_up_table[competitor.sku].competitors.append(competitor)
        else:
            print("Something wierd happend with the competitor product: " + competitor['sku'])
    
    
    response = jsonify({sku_product: our_product.toDict() for sku_product, our_product in look_up_table.items()})
    response.status_code = 200 if products else 404
    return response

@products_blueprint.route('/ours', methods=['POST'])
@token_required
def handleCreateOurProduct(user_data: dict[str, str]):
    request_data = request.get_json()
    err:Exception = None
    new_product:models.Product = None
    
    item_data = request_data.get('item_data', None)
    item_sku = request_data.get('sku', None)
    
    if not item_data or not item_sku:
        response = jsonify({"message": "No data provided"})
        response.status_code = 400
        return response
    
    new_product, err = workflows.creators.createProductFromMeliData(item_data, item_sku)
    new_product.competes_with = ""
    if err:
        print(f"Error creating product: {err}")
        return make_response("Error creating product", 500)
    
    if  new_product.seller_id != service_config.OWNER_ACCOUNT_ID:
        return make_response("Trying to create a competitor product as our product", 421)
    
    err = repository.products.insert(new_product) # if returns !None, must likely means that the product already exists
    if err:
        print(f"Error inserting product: {err}")
        response = jsonify({"message": "Error inserting product data into database", "error": str(err)})
        response.status_code = 402 # this is probably a duplicate product error
        return response

    # Emit domain event
    creator: str =user_data.get('username', 'unkown-user')
    workflows.notifiers.emitProductCompetitorsUpdated(creator, f"'{creator}' added a new product '{new_product.meli_id}' to the tracked products database")
    
    return make_response("ok", 201)
    
@products_blueprint.route('/performance-records', methods=['GET'])
@token_required
def handleGetPerformanceRecords():
    product_type = request.args.get('type', '*')
    
    records = {}
    for r in repository.performance_records.getAllPerformanceRecords():
        if not r.is_completed or (product_type != '*' and r.type != product_type):
            continue
        records[r.product_id] = [r] + records.get(r.product_id, [])
    
    # records == {product_id: [pr_n, pr_n-1, pr_n-2, ...]} where pr_n is the most recent performance record
    response_body = {
        "records": records,
        "recorded_between": repository.performance_records.getRecordedDateRange()
    }
    response = jsonify(response_body)
    response.status_code = 200 if records else 404
    return response

@products_blueprint.route('/products_data/ours', methods=['GET'])
@token_required
def getOurProductsData():
    """ 
        Gets different parameters in the uri, returns a list of products_id and the fields requested
    """
    if request.args == None:
        return make_response(jsonify({"message": "No parameters were requested"}), 406)
    
    fields_requested = list(request.args.keys())
    our_products = repository.products.getOurProducts()
    products_data:List[Dict] = []
    
    for product in our_products:
        product_row = {field_name: product[field_name] for field_name in fields_requested}
        product_row["product_id"] = product.product_id
        products_data.append(product_row)
    
    response = jsonify(products_data)
    return response

@products_blueprint.route('/products_data/match', methods=['GET'])
@token_required
def getProductByField():
    """ 
        get all products that match a requested set of fields
    """
    if request.args == None:
        return make_response(jsonify({"message": "No parameters were requested"}), 400)
    
    fields_requested = request.args
    products:list[models.Product] = repository.products.getAllProducts()
    matched_products:list[models.Product] = []
    for product in products:
        if all(product[field_name] == fields_requested[field_name] for field_name in fields_requested):
            matched_products.append(product)
    
    response = jsonify(matched_products)
    return response

@products_blueprint.route('/', methods=['DELETE'])
@token_required
def handleDeleteProduct(user_data: dict[str, str]):
    request_data = request.get_json()
    if not request_data:
        response = jsonify({"message": "No data provided"})
        response.status_code = 400
        return response
    
    product_id = request_data['product_id']
    product:models.Product = repository.products.getProductById(product_id)
    repository.products.updateStatus(product, "deleted")
    
    # Emit domain event
    creator: str =user_data.get('username', 'unkown-user')
    workflows.notifiers.emitCompetitorDeleted(creator, f"'{creator}' deleted product '{product.meli_id}'")
    
    
    return make_response("ok", 200)
        
@products_blueprint.route('/competitors', methods=['GET'])
@token_required
def handleGetCompetitors():
    """ 
        Returns a list of all of our products with a list of their competitors.
    """
    product_id = request.args.get('product_id')
    if product_id == None:
        return make_response(jsonify({"message": "No product_id was provided"}), 406)
    
    competitors:list[models.Product] = repository.products.getProductCompetitors(product_id)
    
    response = jsonify([competitor.toDict() for competitor in competitors])
    response.status_code = 200 if competitors else 404
    return response





        
    
    
    





    