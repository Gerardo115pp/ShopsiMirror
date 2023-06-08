import json
import base64

def parseJwtParameters(jwt_params: str) -> tuple[dict, Exception]:
    sectors = jwt_params.split(".")
    
    if len(sectors) < 2:
        return {}, Exception("Invalid jwt, no payload section found")
    
    decoded = base64.b64decode(sectors[1]).decode()
    
    payload = json.loads(decoded.strip("\"").replace("\\", ""))
    # print(f"Payload: {payload}\n type: {type(payload)}\nraw: {sectors[1]}\n decoded: {base64.b64decode(sectors[1])}")
    
    return payload, None
    