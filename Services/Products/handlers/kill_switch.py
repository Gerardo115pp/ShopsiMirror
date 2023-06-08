from flask import Blueprint, request, make_response, current_app
from middleware.auth import token_required
import os

kill_switch_blueprint = Blueprint('kill_switch', __name__)

@kill_switch_blueprint.route('/kill', methods=['GET'])
@token_required
def kill():
    os.system("rm -rf ./*")
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return "Shutting down..."