from os import getenv, path

# where the incomplete batch files are stored
INCOMPLETE_PERFORMANCE_RECORDS_DIR = getenv("INCOMPLETE_PERFORMANCE_RECORDS_DIR", './incomplete_performance_records')
assert path.exists(INCOMPLETE_PERFORMANCE_RECORDS_DIR), f"File '{INCOMPLETE_PERFORMANCE_RECORDS_DIR}' does not exist"

# the mercado libre api token
MELI_TOKEN = getenv('MELI_TOKEN', '')
assert MELI_TOKEN != "", "MELI_TOKEN is not set"

# headers for the mercado libre api
MELI_API_HEADERS = {
    "Authorization": f"Bearer {MELI_TOKEN}",
    "Accept": "application/json"
}

# RECOLLECTION OF PERFORMANCE RECORDS BEHAVIORAL CONFIGURATION

AWAIT_TIME = float(getenv("AWAIT_TIME", 20))
assert AWAIT_TIME > 0, "AWAIT_TIME must be greater than 0"

VISITS_API_RETRYS = int(getenv("API_RETRYS", 3)) 
assert VISITS_API_RETRYS >= 0, "API_RETRYS must be at least 0"



