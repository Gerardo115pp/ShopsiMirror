from .mysql_utils import MYSQL_CONFIG, MysqlConnection
from typing import List, Dict
from models import PerformanceRecord, IncompletePerformanceRecord, Reports, ReportData, PerformanceReportRow

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
        
    def getRecordedDateRange(self) -> dict[str, str]:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT MIN(recorded_date) AS `first`, MAX(recorded_date) AS `last` FROM `product_performance_records`;"
            cursor.execute(sql)
            row = cursor.fetchone()
        
        return row
        
    def getAllPerformanceRecords(self) -> list[PerformanceRecord]:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT `pr`.*, `p`.`type` AS `type`  FROM `product_performance_records` `pr` LEFT JOIN `products` `p` ON `pr`.`measures`=`p`.`product_id`;"
            cursor.execute(sql)
            rows = cursor.fetchall()
        
        records = []
        for row in rows:
            perfromance_record = PerformanceRecord.recreate(**row)
            records.append(perfromance_record)
        
        return records
    
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
    
    def getReportsList(self) -> tuple[Reports, Exception]:
        err: Exception = None
        reports: Reports = None
        
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT * FROM `performance_reports`;"
            cursor.execute(sql)
            rows = cursor.fetchall()
        try:
            reports_list = [ReportData.recreate(**row) for row in rows]
            reports = Reports.create(reports_list)
        except Exception as e:
            print(f"error while creating reports list: {e}")
            err = e
        return reports, err
    
    def getPerformanceReportBySerial(self, serial: int) -> tuple[list[PerformanceReportRow], Exception]:
        performance_report: list[PerformanceReportRow] = None
        err:Exception = None
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT `p`.`name` AS `name`,`p`.`initial_price` AS `initial_price`,`p`.`condition` AS `condition`,`p`.`sku` AS `sku`,`p`.`status` AS `status`,`p`.`competes_with` = '' AS `is_ours`,`p`.`meli_url` AS `meli_url`,`pr`.`recorded_date` AS `recorded`,`pr`.`visits` AS `visits`,`pr`.`sales` AS `sales`,`pr`.`current_price` AS `current_price`,`pr`.`stock` AS `stock`,`pr`.`has_discount` AS `has_discount`, `p`.`meli_id` AS `meli_id` from `products` `p` left join `product_performance_records` `pr` on `p`.`product_id`=`pr`.`measures` where `pr`.`serial`={serial};" # the complicated query
            cursor.execute(sql)
            rows = cursor.fetchall()
            try:
                performance_report = [PerformanceReportRow.create(**row) for row in rows]
            except Exception as e:
                print(f"error while creating performance report: {e}")
                err = e
        return performance_report, err
        