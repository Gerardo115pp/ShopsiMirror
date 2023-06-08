from HttpMessages import internals
import models

def emitProductAdded(actor_identifier: str, description: str) -> None:
    new_event:models.SystemEvent = models.SystemEvent.createSystemEvent(description, models.event_types.product_added, actor_identifier)
    
    internals.emitEvent(new_event)
    
def emitProductUpdated(actor_identifier: str, description: str) -> None:
    new_event:models.SystemEvent = models.SystemEvent.createSystemEvent(description, models.event_types.product_updated, actor_identifier)
    
    internals.emitEvent(new_event)
    
def emitRapidReportRequested(actor_identifier: str, description: str) -> None:
    new_event:models.SystemEvent = models.SystemEvent.createSystemEvent(description, models.event_types.rapid_report_requested, actor_identifier)
    
    internals.emitEvent(new_event)
    
def emitRapidReportCreated(actor_identifier: str, description: str) -> None:
    new_event:models.SystemEvent = models.SystemEvent.createSystemEvent(description, models.event_types.rapid_report_created, actor_identifier)
    
    internals.emitEvent(new_event)
    
def emitProductsDatabaseStatusUpdated(actor_identifier: str, description: str) -> None:
    new_event:models.SystemEvent = models.SystemEvent.createSystemEvent(description, models.event_types.products_database_status_updated, actor_identifier)
    
    internals.emitEvent(new_event)
    
def emitProductSearchPerformed(actor_identifier: str, description: str) -> None:
    new_event:models.SystemEvent = models.SystemEvent.createSystemEvent(description, models.event_types.product_search_performed, actor_identifier)
    
    internals.emitEvent(new_event)
    
def emitProductCompetitorsUpdated(actor_identifier: str, description: str) -> None:
    new_event:models.SystemEvent = models.SystemEvent.createSystemEvent(description, models.event_types.product_competitors_updated, actor_identifier)
    
    internals.emitEvent(new_event)

def emitCompetitorDeleted(actor_identifier: str, description: str) -> None:
    new_event:models.SystemEvent = models.SystemEvent.createSystemEvent(description, models.event_types.competitor_deleted, actor_identifier)
    
    internals.emitEvent(new_event)

def emitCreatedCustomQuery(actor_identifier: str, description: str) -> None:
    new_event:models.SystemEvent = models.SystemEvent.createSystemEvent(description, models.event_types.created_custom_query, actor_identifier)
    
    internals.emitEvent(new_event)
    
def emitDeletedCustomQuery(actor_identifier: str, description: str) -> None:
    new_event:models.SystemEvent = models.SystemEvent.createSystemEvent(description, models.event_types.deleted_custom_query, actor_identifier)
    
    internals.emitEvent(new_event)
    
def emitNewProductTracked(actor_identifier: str, description: str) -> None:
    new_event:models.SystemEvent = models.SystemEvent.createSystemEvent(description, models.event_types.new_product_tracked, actor_identifier)
    
    internals.emitEvent(new_event)
    