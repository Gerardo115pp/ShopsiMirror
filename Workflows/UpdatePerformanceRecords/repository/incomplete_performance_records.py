from typing import List, Dict, Any
from models import PerformanceRecord, IncompletePerformanceRecord

incomplete_performance_record_repository_interface = [
    "getCurrentBatch",
    "removeIPR",
    "saveBatch",
    "isBatchComplete",
    "getCurrentSerial",
    "updateIPR"
]

def checkMethodImplemented(cls: Any, method_name: str) -> bool:
    # hoisted function, definition should be in the __init__.py file
    raise NotImplementedError("This function wasnt defined")

class IncompletePerformanceRecordRepoMeta(type):
    """
        Defines behavioral contract of the Incomplete Performance Records Repository. Dont use directly
    """
    
    def __instancecheck__(cls, __instance: Any) -> bool:
        return cls.__subclasscheck__(type(__instance))
    
    def __subclasscheck__(cls, __subclass: type) -> bool:
        # return (hasattr(__subclass, "performanceRecordExists") and callable(getattr(__subclass, "performanceRecordExists"))
        return all(checkMethodImplemented(cls, method_name) for method_name in incomplete_performance_record_repository_interface)
    
class IncompletePerformanceRecordRepository(metaclass=IncompletePerformanceRecordRepoMeta):
    """
        Defines behavioral contract of the Incomplete Performance Records Repository. Dont use directly
    """
    
    def getCurrentBatch(self) -> List[IncompletePerformanceRecord]:
        raise NotImplementedError("This method wasnt implemented")
    
    def removeIPR(self, ipr: IncompletePerformanceRecord) -> None:
        raise NotImplementedError("This method wasnt implemented")
    
    def saveBatch(self, batch: List[IncompletePerformanceRecord], batch_filename:str=None) -> None:
        raise NotImplementedError("This method wasnt implemented")
    
    def isBatchComplete(self, serial:int=-1) -> bool:
        raise NotImplementedError("This method wasnt implemented")
    
    def getCurrentSerial(self) -> int:
        raise NotImplementedError("This method wasnt implemented")
    
    def updateIPR(self, ipr: IncompletePerformanceRecord) -> None:
        raise NotImplementedError("This method wasnt implemented")
    
implementation: IncompletePerformanceRecordRepository = None

def setRepository(repo: IncompletePerformanceRecordRepository) -> None:
    global implementation
    assert isinstance(repo, IncompletePerformanceRecordRepository), f"repo must be a IncompletePerformanceRecordRepository, not {type(repo)}"
    implementation = repo
    
def getCurrentBatch() -> List[IncompletePerformanceRecord]:
    return implementation.getCurrentBatch()

def removeIPR(ipr: IncompletePerformanceRecord) -> None:
    implementation.removeIPR(ipr)

def saveBatch(batch: List[IncompletePerformanceRecord], batch_filename:str=None) -> None:
    implementation.saveBatch(batch, batch_filename)
    
def isBatchComplete(serial:int=-1) -> bool:
    return implementation.isBatchComplete(serial)
    
def getCurrentSerial() -> int:
    return implementation.getCurrentSerial()

def updateIPR(ipr: IncompletePerformanceRecord) -> None:
    implementation.updateIPR(ipr)