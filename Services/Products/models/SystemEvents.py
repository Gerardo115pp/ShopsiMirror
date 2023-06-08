from dataclasses import dataclass, asdict
import enum


EventTypes = enum.Enum('EventType', 'product_added product_updated rapid_report_requested rapid_report_created products_database_status_updated product_search_performed product_competitors_updated competitor_deleted created_custom_query deleted_custom_query new_product_tracked')


@dataclass
class SystemEvent:
    description: str
    event_type: EventTypes
    actor: str
    
    def toJson(self):
        return {
            "description": self.description,
            "type": self.event_type.name,
            "actor": self.actor
        }
        
    @staticmethod
    def createSystemEvent(description: str, event_type: EventTypes, actor: str) -> 'SystemEvent':
        return SystemEvent(description, event_type, actor)
    