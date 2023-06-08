from typing import List, Dict, Any
from models import PerformanceRecord, IncompletePerformanceRecord

performance_record_repository_interface = [
    "insert",
    "getNewestBatch",
    "getCurrentBatchSerial"
]

def checkMethodImplemented(cls: Any, method_name: str) -> bool:
    # hoisted function, definition should be in the __init__.py file
    raise NotImplementedError("This function wasnt defined")

class PerformanceRecordRepoMeta(type):
    """
        Defines behavioral contract of the Performance Record Repository. Dont use directly
    """
    
    def __instancecheck__(cls, __instance: Any) -> bool:
        return cls.__subclasscheck__(type(__instance))
    
    def __subclasscheck__(cls, __subclass: type) -> bool:
        # return (hasattr(__subclass, "performanceRecordExists") and callable(getattr(__subclass, "performanceRecordExists"))
        return all(checkMethodImplemented(cls, method_name) for method_name in performance_record_repository_interface)
    
class PerformanceRecordRepository(metaclass=PerformanceRecordRepoMeta):
    """
        Defines behavioral contract of the Performance Record Repository. Dont use directly
    """
    
    def insert(self, performance_record: IncompletePerformanceRecord, serial: int) -> None:
        raise NotImplementedError("This method wasnt implemented")
    
    def getNewestBatch(self) -> List[PerformanceRecord]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getCurrentBatchSerial(self) -> int:
        raise NotImplementedError("This method wasnt implemented")
    
implementation: PerformanceRecordRepository = None

def setRepository(repo: PerformanceRecordRepository) -> None:
    global implementation
    assert isinstance(repo, PerformanceRecordRepository), f"repo must be a PerformanceRecordRepository, not {type(repo)}"
    implementation = repo
    
def insert(performance_record: IncompletePerformanceRecord, serial: int) -> None:
    implementation.insert(performance_record, serial)
    
def getNewestBatch() -> List[PerformanceRecord]:
    return implementation.getNewestBatch()

def getCurrentBatchSerial() -> int:
    return implementation.getCurrentBatchSerial()
    