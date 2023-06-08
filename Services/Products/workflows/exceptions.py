from HttpMessages.exceptions import *

class ProductNotFoundError(MeliApiError):
    def __init__(self, message):
        super().__init__(message, 404)
