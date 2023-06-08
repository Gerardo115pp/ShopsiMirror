from dataclasses import dataclass
import Config as service_config
import redis

@dataclass
class REDIS_CONFIG:
    host: str
    port: int
    password: str
    db: int

    @staticmethod
    def createFromEnv() -> 'REDIS_CONFIG':
        return REDIS_CONFIG(
            host=service_config.REDIS_HOST,
            port=service_config.REDIS_PORT,
            password=service_config.REDIS_PASSWORD,
            db=0
        )
        
class RedisConnection:
    def __init__(self, config: REDIS_CONFIG=None):
        config = config or REDIS_CONFIG.createFromEnv()
        self.conn = redis.Redis(
            host=config.host,
            port=config.port,
            password=config.password,
            db=config.db
        )
        
    def __enter__(self) -> redis.Redis:
        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.conn.close()
