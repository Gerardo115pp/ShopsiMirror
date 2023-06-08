from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
import Config as service_config
import json

def allArgsPresent(obj: object, args: list[str]) -> bool:
    """ 
        this method should be reassigned from the __init__.py file
    """
    raise NotImplementedError("this shouldnt happen")

@dataclass
class MeliAuth:
    code: str
    redirect_uri: str
    client_id: str
    client_secret: str
    grant_type: str = "authorization_code"
    access_token: str = None
    token_type: str = None
    expires_in: float = 0
    scope: str = None
    user_id: int = None
    refresh_token: str = None
    app_user: str = None
    
    @staticmethod
    def recreate(**kwargs) -> "MeliAuth":
        assert allArgsPresent(MeliAuth, kwargs), "Missing arguments"
        
        return MeliAuth(**kwargs)
    
    @property
    def Duration(self) -> float:
        return self.expires_in - datetime.now().timestamp()  
    
    @Duration.setter
    def Duration(self, duration:float):
        self.expires_in = (datetime.now() + timedelta(seconds=duration)).timestamp()
    
    @staticmethod
    def loadTokens() -> list['MeliAuth']:
        tokens_data = service_config.loadTokens()
        return [MeliAuth.recreate(**token_data) for token_data in tokens_data]
    
    def toDict(self) -> dict: 
        return asdict(self)
    
    def toJson(self) -> str:
        return json.dumps(self.toDict())
    
    def isActive(self) -> bool:
        return self.Duration > 10
    
    def isValid(self) ->bool:
        valid = self.isActive() and self.access_token is not None
        expiration_date = datetime.fromtimestamp(self.expires_in)
        print(f"token is valid: {valid}, expires in: {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}")
        return valid
