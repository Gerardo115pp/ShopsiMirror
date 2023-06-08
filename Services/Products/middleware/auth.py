from flask import Flask, request, jsonify, make_response
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable
from inspect import getfullargspec
import Config as service_config
import jwt
import os

def token_required(f: Callable) -> Callable:
    jwt_secret = os.getenv('JWT_SECRET')
    assert jwt_secret is not None, 'JWT_SECRET must be set'
    
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', "")
        token = token.removeprefix('Bearer ')
        
        if token == "":
            print("No token provided")
            return jsonify({"message": "Missing token"}), 401

        if service_config.DOMAIN_SECRET == token:
            user_data = {
                "user_id": "domain",
                "username": "domain",
                "email": ""
            }
            
            if len(getfullargspec(f).args) == 1:
                return f(user_data, *args, **kwargs)
            else:
                return f(*args, **kwargs)
            


        print(f"Token: {token}\n JWT_SECRET: {jwt_secret}")
        try:
            jwt_header = jwt.get_unverified_header(token)
            data = jwt.decode(token, jwt_secret, algorithms=[jwt_header['alg']])
            user_data = {
                "user_id": data.get('user_id', None),
                "username": data.get('username', None),
                "email": data.get('email', None)
            }
            assert user_data is not None, 'user_id must be set'
        except Exception as e:
            print(f"Error decoding token: {e}")
            return jsonify({"message": f"Invalid token: {e}"}), 401
        
        if len(getfullargspec(f).args) == 1:
            return f(user_data, *args, **kwargs)
        else:
            return f(*args, **kwargs)

    return decorated
