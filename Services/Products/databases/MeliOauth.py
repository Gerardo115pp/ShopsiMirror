import Config as service_config
from datetime import datetime
from models import MeliAuth
from os.path import exists
import HttpMessages as http_messages
import json

class MeliOauthRepository:
    def __init__(self):
        self.tokens = self._loadTokens()
    
    def _loadTokens(self) -> list[MeliAuth]:
        loaded_tokens = []
        if exists(service_config.TOKENS_DATA):
            with open(service_config.TOKENS_DATA, 'r') as f:
                tokens_data = json.load(f)
                loaded_tokens = [MeliAuth.recreate(**token_data) for token_data in tokens_data]
        return loaded_tokens
    
    def _saveTokens(self):
        tokens_data = [token.toDict() for token in self.tokens]
        with open(service_config.TOKENS_DATA, 'w') as f:
            json.dump(tokens_data, f)
    
    def insert(self, oauth_token: MeliAuth) -> Exception:
        err:Exception = None
        new_tokens = [t for t in self.tokens if t.app_user != oauth_token.app_user]
        if len(new_tokens) != len(self.tokens):
            print(f"WARNINIG: Overwriting token for user: {oauth_token.app_user}")
        
        new_tokens.append(oauth_token)
        self.tokens = new_tokens
        self._saveTokens()
        return err
        
    
    def getTokenByUserId(self, user_id: str) -> tuple[MeliAuth, Exception]:
        token = None
        err:Exception = None
        for t in self.tokens:
            if t.app_user == user_id:
                token = t
                break
            
        if not token:
            print(f"Token not found for user: {user_id}")
            return None, Exception("Token not found")
            
        print(f"token is valid: {token.isValid()}")
        if token and not token.isValid():
            print(f"INFO: Token for user {user_id} is not valid, trying to refresh")
            token, err = http_messages.meli_api.refreshAccessToken(token)
            if err:
                return None, err

            err = self.insert(token)
            if err:
                return None, err
            print(f"INFO: Token for user {user_id} was updated")
        
        return token, err    
    
    