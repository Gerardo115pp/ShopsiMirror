from models import PerformanceRecord, IncompletePerformanceRecord, Product
from .mysql_utils import MYSQL_CONFIG, MysqlConnection
import Config as workflow_config
from typing import List, Dict, Tuple
import json
import os

class IncompletePerformanceRecordRepository:
    def __init__(self, config: MYSQL_CONFIG=None):
        if not config:
            config = MYSQL_CONFIG.createFromEnv()
        self.workflow_config = workflow_config
        self.config = config

    
    def __createNewBatch(self) -> Tuple[List[IncompletePerformanceRecord], Exception]:
        current_serial = self.getCurrentSerial()
        assert self.isBatchComplete(serial=current_serial), f"Trying to create a new batch when the current batch is not complete: {current_serial}"
        
        current_serial += 1 # new batch serial
        
        print(f"Creating new batch  '{current_serial}'")
        new_batch:List[IncompletePerformanceRecord] = [IncompletePerformanceRecord.create(product_id=p.product_id, meli_id=p.meli_id, meli_url=p.meli_url, serial=current_serial) for p in self.__getActiveProducts()]
        self.saveBatch(new_batch)
        return new_batch, None
    
            
    def __getActiveProducts(self) -> List[Product]:
        # we cant use the ProductRepository here because it would create a circular dependency
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT * FROM `products` WHERE `status`='active' AND `meli_url`!='no permalink';"
            cursor.execute(sql)
            rows = cursor.fetchall()
        
        active_products = []
        for row in rows:
            product = Product.recreate(**row)
            active_products.append(product)
        
        return active_products
    
    def __getMaxSerial(self) -> int:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT MAX(serial) AS `max_serial` FROM `product_performance_records`;"
            cursor.execute(sql)
            row = cursor.fetchone()
        
        max_serial = row["max_serial"]
        return max_serial

    def getCurrentBatch(self) -> List[IncompletePerformanceRecord]:
        current_batch = []
        
        current_serial = self.getCurrentSerial()
        if self.isBatchComplete(serial=current_serial):
            current_batch, _ = self.__createNewBatch()
            return current_batch

        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT p.product_id, pr.serial, p.meli_id, p.meli_url, pr.visits, pr.sales, pr.stock, pr.has_discount as has_discounts, pr.current_price FROM `product_performance_records` `pr` LEFT JOIN `products` `p` ON `pr`.`measures`=`p`.`product_id` WHERE `pr`.`serial`={current_serial} AND `pr`.`is_completed`=0;"
            cursor.execute(sql)
            rows = cursor.fetchall()
        
        current_batch = [IncompletePerformanceRecord.recreate(**row) for row in rows]
        
        return current_batch
    
    def getCurrentSerial(self) -> int:
        current_serial = self.__getMaxSerial()
        # this function used to check if there was an incomplete batch by checking if a batch_n.json file existed, but now everyting is stored in the database, including incomplete batches
        # keeping this function for backwards compatibility
            
        return current_serial
    
    def isBatchComplete(self, serial:int=-1) -> bool:
        sql = f"SELECT COUNT(*) AS `count` FROM `product_performance_records` WHERE `serial`={serial} AND is_completed=0;"
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            row = cursor.fetchone()
        
        return row["count"] == 0
    
    def removeIPR(self, ipr: IncompletePerformanceRecord) -> None:
        assert not ipr.isCompleted, f"Trying to remove a completed IPR: {ipr.product_id},{ipr.serial}"
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"DELETE FROM `product_performance_records` WHERE `serial`={ipr.serial} and `measures`='{ipr.product_id}' and `is_completed`=0;"
            cursor.execute(sql)
            conn.commit() 
    
    def saveBatch(self, batch: List[IncompletePerformanceRecord]) -> None:
        if len(batch) == 0:
            return
        current_serial = batch[0].serial
        print(f"Saving batch {current_serial}")
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            for ipr in batch:
                sql = f"INSERT INTO `product_performance_records` (`serial`, `measures`) VALUES ({current_serial}, '{ipr.product_id}');"
                cursor.execute(sql)
            conn.commit()
            
    def updateIPR(self, ipr: IncompletePerformanceRecord) -> None:
        assigment_list = ""
        assigment_list += f" `visits`={ipr.visits}," if ipr.visits != -1 else ""
        assigment_list += f" `sales`={ipr.sales}," if ipr.sales != -1 else ""
        assigment_list += f" `current_price`={ipr.current_price}," if ipr.current_price != -1 else ""
        assigment_list += f" `stock`={ipr.stock}," if ipr.stock != -1 else ""
        assigment_list += f" `has_discount`={ipr.has_discounts}," if ipr.has_discounts else ""
        
        assigment_list = assigment_list[:-1] # remove last comma
        sql_update = f"UPDATE `product_performance_records` SET {assigment_list} WHERE `serial`={ipr.serial} and `measures`='{ipr.product_id}' and `is_completed`=0 LIMIT 1;"
        print(f"Updating IPR: {ipr.product_id},{ipr.serial}\n {sql_update}")
        
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql_update)
            conn.commit()
        
            
    
    
    
    
    