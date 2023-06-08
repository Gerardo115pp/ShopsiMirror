import requests
import models
import Config as service_config

def emitEvent(event: models.SystemEvent) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": service_config.DOMAIN_SECRET
    }
    
    notification_system_url = f"{service_config.NOTIFICATIONS_SERVER}/events"
    print(f"Sending event to {notification_system_url} with headers {headers} and body {event.toJson()}")
    
    requests.post( notification_system_url, headers=headers, json=event.toJson())