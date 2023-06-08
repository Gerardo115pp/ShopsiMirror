from .IncompletePerformanceRecord import IncompletePerformanceRecordRepository
from .PerformanceRecord import PerformanceRecordRepository
from .Products import ProductRepository
from .mysql_utils import MYSQL_CONFIG

def createProductRepository() -> ProductRepository:
    return ProductRepository(MYSQL_CONFIG.createFromEnv())

def createPerformanceRecordRepository() -> PerformanceRecordRepository:
    return PerformanceRecordRepository(MYSQL_CONFIG.createFromEnv())

def createIncompletePerformanceRecordRepository() -> IncompletePerformanceRecordRepository:
    return IncompletePerformanceRecordRepository(MYSQL_CONFIG.createFromEnv())