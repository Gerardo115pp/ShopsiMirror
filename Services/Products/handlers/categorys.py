from flask import Blueprint, request, make_response, current_app, jsonify
from middleware.auth import token_required
import Config as service_config
import repository
import models
import workflows 

categories_blueprint = Blueprint('categories', __name__)

@categories_blueprint.route('/', methods=['GET'])
def getCategories():
    return make_response("Not implemented", 501)

@categories_blueprint.route('/trends', methods=['GET'])
@token_required
def getCategoryTrends(user_data: dict[str, str]):
    category_id = request.args.get('category_id', '')
    err: Exception = None
    print(f"Getting category trends for user: {user_data}")
    user_id: str = user_data.get('user_id', '')
    assert user_id, "Token didnt contain user_id"
    
    if not category_id:
        return make_response("No category id provided", 400)
    
    meli_auth: models.MeliAuth = None
    meli_auth, err = repository.meli_oauth_tokens.getTokenByUserId(user_id)
    if err:
        print(f"Error getting meli auth for user {user_id}: {err}")
        return make_response("Server error, sorry for the inconvenience", 401)
    
    if not meli_auth:
        return make_response("No oauth token found", 401)
    
    if not meli_auth.isValid():
        return make_response("Token expired", 403)
    
    category: models.CategoryData  = None
    trends: list[models.Trend] = None
    
    category, err = workflows.collectors.getCategoryData(category_id, meli_auth)
    if err:
        print(f"Error getting category data: {err}")
        return make_response("Server error sorry for the inconvinience", 500)
    
    trends, err = workflows.collectors.getCategoryTrends(category.category_id, meli_auth)
    if err:
        print(f"Error getting category trends: {err}")
        return make_response("Server error sorry for the inconvinience", 500)
    
    category_trends: models.CategoryTrends = models.CategoryTrends(category=category, trends=trends)
    return jsonify(category_trends.toDict())