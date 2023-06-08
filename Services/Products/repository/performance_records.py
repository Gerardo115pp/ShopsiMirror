from typing import List, Dict, Any
from models import PerformanceRecord, IncompletePerformanceRecord, Reports, PerformanceReportRow

performance_record_repository_interface = [
    "insert",
    "getNewestBatch",
    "getCurrentBatchSerial",
    "getPerformanceReport",
    "getCompetitorProducts",
    "getOurProducts",
    "getReportsList",
    "getPerformanceReportBySerial",
    "getAllPerformanceRecords",
    "getRecordedDateRange"
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
        for method_name in performance_record_repository_interface:
            if not checkMethodImplemented(cls, method_name):
                print(f"Method {method_name} not implemented in {__subclass}")
                return False
        return True
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
    
    def getPerformanceReport(self) -> List[Dict]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getCompetitorProducts(self) -> List[Dict]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getOurProducts(self) -> List[Dict]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getReportsList(self) -> tuple[Reports, Exception]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getPerformanceReportBySerial(self, serial: int) -> tuple[list[PerformanceReportRow], Exception]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getAllPerformanceRecords(self) -> list[PerformanceRecord]:
        raise NotImplementedError("This method wasnt implemented")
    
    def getRecordedDateRange(self) -> dict[str, str]:
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
    
def getPerformanceReport() -> List[Dict]:
    return implementation.getPerformanceReport()

def getCompetitorProducts() -> List[Dict]:
    return implementation.getCompetitorProducts()

def getOurProducts() -> List[Dict]:
    return implementation.getOurProducts()

def getReportsList() -> tuple[Reports, Exception]:
    return implementation.getReportsList() 

def getPerformanceReportBySerial(serial: int) -> tuple[list[PerformanceReportRow], Exception]:
    return implementation.getPerformanceReportBySerial(serial)

def getAllPerformanceRecords() -> list[PerformanceRecord]:
    return implementation.getAllPerformanceRecords()

def getRecordedDateRange() -> dict[str, str]:
    return implementation.getRecordedDateRange()