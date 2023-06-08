from dataclasses import dataclass, asdict
from .Product import Product
from .PerformanceRecord import PerformanceRecord
from datetime import datetime, date

def allArgsPresent(obj: object, args: list[str]) -> bool:
    """ 
        this method should be reassigned from the __init__.py file
    """
    raise NotImplementedError("this shouldnt happen")

@dataclass
class ReportData:
    last_update: str
    serial: int
    records: int
    completed: int
    
    @staticmethod
    def create(**kwargs) -> "ReportData":
        assert allArgsPresent(ReportData, kwargs), f"not all args are present: {kwargs}"
        
        return ReportData(**kwargs)
    
    @staticmethod
    def recreate(**kwargs) -> "ReportData":
        if "last_update" in kwargs and isinstance(kwargs["last_update"], datetime):
            kwargs["last_update"] = kwargs["last_update"].strftime("%Y-%m-%d %H:%M:%S")
        
        assert allArgsPresent(ReportData, kwargs), f"not all args are present: {kwargs}"
        
        return ReportData(**kwargs)
    
    def toDict(self) -> dict:
        return asdict(self)
    
@dataclass
class Reports:
    reports: list[ReportData]
    
    @staticmethod
    def create(reports: list[ReportData]) -> "Reports":
        """ 
            exclude reports that where done in the same day and those where records!=completed
        """
        # clean reports
        reports = [report for report in reports if report.records == report.completed]
        date_reports_lookup = {} # key: date, value: ReportData, keep the last report of the day
        for report in reports:
            report_date = report.last_update.split(" ")[0]
            date_reports_lookup[report_date] = report
            
        reports = list(date_reports_lookup.values())
        return Reports(reports)
    
    def toDict(self) -> dict:
        return [report.toDict() for report in self.reports]
        
        
@dataclass
class PerformanceReportRow:
    name: str
    initial_price: float
    condition: str
    sku: str
    status: str
    is_ours: bool
    meli_url: str
    meli_id: str
    recorded: str
    visits: int
    sales: int
    current_price: float
    stock: int
    has_discount: bool
    
    @staticmethod
    def create(**kwargs) -> "PerformanceReportRow":
        if 'meli_id' not in kwargs:
            kwargs['meli_id'] = 'unknown'
        
        assert allArgsPresent(PerformanceReportRow, kwargs), f"not all args are present: {kwargs}"
        if type(kwargs["is_ours"]) != bool:
            kwargs["is_ours"] = bool(kwargs["is_ours"])
        
        
        if type(kwargs["has_discount"]) != bool:
            kwargs["has_discount"] = bool(kwargs["has_discount"])
            
        return PerformanceReportRow(**kwargs)
    
    @staticmethod
    def recreate(**kwargs) -> "PerformanceReportRow":
        return PerformanceReportRow(**kwargs)
    
    @staticmethod
    def toDict(self) -> dict:
        return asdict(self)
        
        
        
        
        
        