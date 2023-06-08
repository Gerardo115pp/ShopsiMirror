from .mysql_utils import MYSQL_CONFIG, MysqlConnection
from typing import List, Dict
from models import Product

class ProductRepository:
    def __init__(self, config: MYSQL_CONFIG=None):
        if not config:
            config = MYSQL_CONFIG.createFromEnv()
            
        self.config = config
        
    def updateStatus(self, product: Product, status: str) -> None:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"UPDATE `products` SET `status`='{status}' WHERE `product_id`='{product.product_id}';"
            cursor.execute(sql)
            conn.commit()
            
    def getActiveProducts(self) -> List[Product]:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT * FROM `products` WHERE `status`='active';"
            cursor.execute(sql)
            rows = cursor.fetchall()
        
        active_products = []
        for row in rows:
            product = Product.recreate(**row)
            active_products.append(product)
        
        return active_products

    def getAllProducts(self) -> List[Product]:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT * FROM `products` where `status`!='deleted';"
            cursor.execute(sql)
            rows = cursor.fetchall()
        
        all_products = []
        for row in rows:
            product = Product.recreate(**row)
            all_products.append(product)
        
        return all_products
    
    def getProductById(self, product_id: str) -> Product:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT * FROM `products` WHERE `product_id`='{product_id}';"
            cursor.execute(sql)
            row = cursor.fetchone()
        
        product = Product.recreate(**row)
        return product
    
    def getActiveProduct(self) -> Product:
        """
        Get a random active product from the database. mainly thought for testing purposes.

        Returns:
            Product: a random active product from the database.
        """
        
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT * FROM `products` WHERE `status`='active' LIMIT 1;"
            cursor.execute(sql)
            row = cursor.fetchone()
        
        product = Product.recreate(**row)
        return product