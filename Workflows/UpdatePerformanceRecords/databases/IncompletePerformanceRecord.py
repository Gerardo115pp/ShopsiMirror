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
            print(f"Using config from env: {config}")
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
        """
        Get the current batch of incomplete performance records. If the current batch is complete, it creates a new one using the __createNewBatch method and returns it.
        
        Returns:
            List[IncompletePerformanceRecord]: current batch of incomplete performance records
        """
        
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
        """ Get the current batch serial, which is the highest serial in the reports table

        Returns:
            int: current batch serial
        """
        
        current_serial = self.__getMaxSerial()
        # this function used to check if there was an incomplete batch by checking if a batch_n.json file existed, but now everyting is stored in the database, including incomplete batches
        # keeping this function for backwards compatibility
            
        return current_serial
    
    def isBatchComplete(self, serial:int=-1) -> bool:
        """ 
            Check if the current batch is complete. A batch is complete if there are no incomplete performance records for that batch
            We know if a performance record is complete with the `is_completed` flag, which is a generated column in the database
            defined as '`is_completed` TINYINT(1) GENERATED ALWAYS AS (`visits`!=-1 AND `sales`!=-1 AND `current_price`!=-1 AND `stock`!=-1) VIRTUAL`'

            Args:
                serial (int, optional): batch serial to check. Defaults to -1.

            Returns:
                bool: True if the batch is complete, False otherwise
        """
        
        sql = f"SELECT COUNT(*) AS `count` FROM `product_performance_records` WHERE `serial`={serial} AND is_completed=0;"
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            row = cursor.fetchone()
        
        return row["count"] == 0
    
    def removeIPR(self, ipr: IncompletePerformanceRecord) -> None:
        """
            Remove an incomplete performance record from the database. This is used when a product cannot be measured, possibly because 
            it was a status other then `active`.

        Args:
            ipr (IncompletePerformanceRecord): incomplete performance record to remove. must not be completed(AKA have all the measures)
        """
        
        assert not ipr.isCompleted, f"Trying to remove a completed IPR: {ipr.product_id},{ipr.serial}"
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"DELETE FROM `product_performance_records` WHERE `serial`={ipr.serial} and `measures`='{ipr.product_id}' and `is_completed`=0;"
            cursor.execute(sql)
            conn.commit() 
    
    def saveBatch(self, batch: List[IncompletePerformanceRecord]) -> None:
        """
            Save(Inserts) a batch of incomplete performance records to the database. this is not meant to be used to update existing records, only to create new ones.

        Args:
            batch (List[IncompletePerformanceRecord]): batch of incomplete performance records to save. These should only include the batch serial and the id  of the product to measure.
        """
        
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
        """
            Update an incomplete performance record in the database. This is used to update the recorded measures of a product.

        Args:
            ipr (IncompletePerformanceRecord): incomplete performance record to update.
        """
        
        assignment_list = ""
        assignment_list += f" `visits`={ipr.visits}," if ipr.visits != -1 else ""
        assignment_list += f" `sales`={ipr.sales}," if ipr.sales != -1 else ""
        assignment_list += f" `current_price`={ipr.current_price}," if ipr.current_price != -1 else ""
        assignment_list += f" `stock`={ipr.stock}," if ipr.stock != -1 else ""
        assignment_list += f" `has_discount`={ipr.has_discounts}," if ipr.has_discounts else ""
        
        assignment_list = assignment_list[:-1] # remove last comma
        sql_update = f"UPDATE `product_performance_records` SET {assignment_list} WHERE `serial`={ipr.serial} and `measures`='{ipr.product_id}' and `is_completed`=0 LIMIT 1;"
        print(f"Updating IPR: {ipr.product_id},{ipr.serial}\n {sql_update}")
        
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql_update)
            conn.commit()
        
            
    
    
    
    
    