from mysql.connector import connect as mysql_connect, connection
from dataclasses import dataclass
import os

@dataclass
class MYSQL_CONFIG:
    user: str
    password: str
    port: int = 3306
    host: str = 'localhost'
    database: str = ''
    
    @staticmethod
    def createFromEnv() -> 'MYSQL_CONFIG':
        return MYSQL_CONFIG(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            port=int(os.environ['MYSQL_PORT']),
            database=os.environ['MYSQL_DB']
        )

class MysqlConnection:
    def __init__(self, config: MYSQL_CONFIG):
        self.conn: connection = mysql_connect(
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
            database=config.database
        )
        
    def __enter__(self) -> connection:
        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.conn.close()