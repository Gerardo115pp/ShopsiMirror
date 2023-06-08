import HttpMessages
import models

def exchangeAccessToken(meli_auth: models.MeliAuth) -> tuple[models.MeliAuth, Exception]:
    """ 
        exchanges the access code for an access token, and returns it
    """
    meli_auth, err = HttpMessages.meli_api.exchangeAccessToken(meli_auth)
    return meli_auth, err