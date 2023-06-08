from .mysql_utils import MYSQL_CONFIG, MysqlConnection
from typing import List, Dict
from models import PerformanceRecord, IncompletePerformanceRecord

class PerformanceRecordRepository:
    def __init__(self, config: MYSQL_CONFIG=None):
        if not config:
            config = MYSQL_CONFIG.createFromEnv()
            
        self.config = config
        
    def getPerformanceReport(self):
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM performance") # view for a very complicated query
            return cursor.fetchall()
    
    def insert(self, performance_record: IncompletePerformanceRecord, batch_serial:int) -> None:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"INSERT INTO `product_performance_records`(`serial`, `visits`, `sales`, `current_price`, `keywords_file`, `stock`, `has_discount`, `measures`)  VALUES ({batch_serial}, {performance_record.visits}, {performance_record.sales}, {performance_record.current_price}, 'TODO', {performance_record.stock}, {performance_record.has_discounts}, '{performance_record.product_id}');"
            cursor.execute(sql)
            conn.commit()
            
    def getNewestBatch(self) -> List[PerformanceRecord]:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT * FROM `product_performance_records` WHERE serial = (SELECT MAX(serial) FROM `product_performance_records`);"
            cursor.execute(sql)
            rows = cursor.fetchall()
        
        newest_batch = []
        for row in rows:
            perfromance_record = PerformanceRecord.recreate(row)
            newest_batch.append(perfromance_record)
        
        return newest_batch
            
    def getCurrentBatchSerial(self) -> int:
        # returns the serial of a yet not existing batch, aka MAX(serial) + 1
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT MAX(serial) AS `max_serial` FROM `product_performance_records`;"
            cursor.execute(sql)
            row = cursor.fetchone()
        
        return row["max_serial"]+1
        