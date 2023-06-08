from os import getenv, path
import json

# the mercado libre app secret
MELI_TOKEN = getenv('MELI_TOKEN', '')
assert MELI_TOKEN != "", "MELI_TOKEN is not set"
# mercado libre app id
APP_ID = getenv('APP_ID', '')
assert APP_ID != "", "APP_ID is not set"

# products server url
PRODUCTS_URL = getenv('PRODUCT_SERVER', '')
assert PRODUCTS_URL != "", "PRODUCT_SERVER is not set"

# oauth server url
OAUTH_URL = getenv('OAUTH_SERVER', '')
assert OAUTH_URL != "", "OAUTH_SERVER is not set"

# client url
BONHART_CLIENT = getenv('BONHART_CLIENT', '')
assert BONHART_CLIENT != "", "BONHART_CLIENT is not set"

# where tokens are stored
TOKENS_DATA = getenv('MELI_TOKENS_PATH', '')
assert TOKENS_DATA != "", "MELI_TOKENS_PATH is not set"

# where the data files are stored
DATA_FILES = getenv('DATA_FOLDER', '')
assert DATA_FILES != "", "DATA_FOLDER is not set"

OWNER_ACCOUNT_ID = int(getenv('OWNER_ACCOUNT_ID', '-1'))
assert OWNER_ACCOUNT_ID != -1, "OWNER_ACCOUNT_ID is not set"

# headers for the mercado libre api
MELI_API_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Authorization": f"Bearer {MELI_TOKEN}",
    "Accept": "application/json"
}

FLASK_SECRET_KEY = getenv('FLASK_SECRET_KEY', '')
assert FLASK_SECRET_KEY != "", "FLASK_SECRET_KEY is not set"


JWT_SECRET_KEY = getenv("JWT_SECRET", "")
assert JWT_SECRET_KEY != "", "JWT_SECRET is not set"

SERVER_HOST = getenv("SERVER_HOST", "0.0.0.0")

SERVER_PORT = getenv("SERVER_PORT", "4500")
SERVER_PORT = int(SERVER_PORT)

EXCEL_PATH = getenv("EXCEL_PATH", "./")

NOTIFICATIONS_SERVER = getenv("INTERNAL_NOTIFICATIONS_SERVER", "")
assert NOTIFICATIONS_SERVER != "", "INTERNAL_NOTIFICATIONS_SERVER is not set"

DOMAIN_SECRET = getenv("DOMAIN_SECRET", "")
assert DOMAIN_SECRET != "", "DOMAIN_SECRET is not set"

__redis_url = getenv("REDIS_URL", "")
assert __redis_url != "", "REDIS_URL is not set"

REDIS_HOST = __redis_url.split(":")[0]
REDIS_PORT = int(__redis_url.split(":")[1])
REDIS_PASSWORD = getenv("REDIS_PASSWORD", "")