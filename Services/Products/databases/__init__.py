from .IncompletePerformanceRecord import IncompletePerformanceRecordRepository
from .PerformanceRecord import PerformanceRecordRepository
from .Products import ProductRepository
from .CustomQuerys import CustomQueryRepository
from .Sellers import SellerRepository
from .MeliOauth import MeliOauthRepository
from .mysql_utils import MYSQL_CONFIG
from .redis_utils import REDIS_CONFIG
from .redis_cache import RedisCache

def createProductRepository() -> ProductRepository:
    return ProductRepository(MYSQL_CONFIG.createFromEnv())

def createPerformanceRecordRepository() -> PerformanceRecordRepository:
    return PerformanceRecordRepository(MYSQL_CONFIG.createFromEnv())

def createIncompletePerformanceRecordRepository() -> IncompletePerformanceRecordRepository:
    return IncompletePerformanceRecordRepository(MYSQL_CONFIG.createFromEnv())

def createSellerRepository() -> SellerRepository:
    return SellerRepository(MYSQL_CONFIG.createFromEnv())

def createMeliOAuthTokenRepository() -> MeliOauthRepository:
    return MeliOauthRepository()

def createCustomQueryRepository() -> CustomQueryRepository:
    return CustomQueryRepository()

def createRedisCache() -> RedisCache:
    return RedisCache(REDIS_CONFIG.createFromEnv())