from flask import Blueprint, request, make_response, current_app, jsonify, redirect
from middleware.auth import token_required
import Config as service_config
import workflows
import repository
from uuid import uuid4
import models

meli_auth_blueprint = Blueprint('meli-auth', __name__)
REDIRECT_URI = f"{service_config.OAUTH_URL}/"
oauth_process_states = {} # {state: user_id,...}


@meli_auth_blueprint.route('/auth-url', methods=['GET'])
@token_required
def getMeliAuthenticationUrl(user_data: dict[str, str]):
    app_id = service_config.APP_ID
    response_type = "code"
    user_id: str = user_data.get('user_id', None)
    assert user_id is not None, 'user_id must be set'
    
    for saved_state, saved_user in oauth_process_states.items():
        if saved_user == user_id:
            del oauth_process_states[saved_state]
            break
    
    state = str(uuid4())
    oauth_process_states[state] = user_id
    
    
    meli_auth_url = f"https://auth.mercadolibre.com.mx/authorization?response_type={response_type}&client_id={app_id}&state={state}&redirect_uri={REDIRECT_URI}"
    return jsonify({"url": meli_auth_url})

@meli_auth_blueprint.route('/', methods=['GET'])
def recieveMeliAuthenticationCode():
    code = request.args.get('code', '')
    state = request.args.get('state', '')
    if not code:
        return make_response("No code provided", 406)
    
    user_id = oauth_process_states.get(state, None)
    if not user_id:
        return make_response("Invalid state", 406)
    
    meli_auth = models.MeliAuth(code=code, redirect_uri=REDIRECT_URI, client_id=service_config.APP_ID, client_secret=service_config.MELI_TOKEN, app_user=user_id)
    meli_auth, err = workflows.auth.exchangeAccessToken(meli_auth)
    if err:
        return make_response(f"Error getting access token: {err}", 500)
    
    repository.meli_oauth_tokens.insert(meli_auth)
    print(f"Token for user {user_id} saved")
    return redirect(f"{service_config.BONHART_CLIENT}/#/system-users")

@meli_auth_blueprint.route('/get-token', methods=['GET'])
@token_required
def getMeliAccessToken(user_data: dict[str, str]):
    user_id: str = user_data.get('user_id', None)
    assert user_id is not None, 'user_id must be set'
    
    meli_auth, err = repository.meli_oauth_tokens.getTokenByUserId(user_id)
    if err:
        return make_response(f"Error getting access token: {err}", 500)
    
    return jsonify(meli_auth.toDict())
