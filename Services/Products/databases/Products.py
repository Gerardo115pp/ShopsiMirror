from .mysql_utils import MYSQL_CONFIG, MysqlConnection
from typing import List, Dict
from models import Product

class ProductRepository:
    def __init__(self, config: MYSQL_CONFIG=None):
        if not config:
            config = MYSQL_CONFIG.createFromEnv()
            
        self.config = config
    
    def insert(self, new_product: Product) -> Exception:
        err:Exception = None
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"INSERT INTO `products` (`meli_id`, `name`, `site_id`, `category_id`, `initial_price`, `secure_thumbnail`, `condition`, `sku`, `status`, `competes_with`, `meli_url`, `domain_id`, `seller_id`) VALUES ('{new_product.meli_id}', '{new_product.name}', '{new_product.site_id}', '{new_product.category_id}', '{new_product.initial_price}', '{new_product.secure_thumbnail}', '{new_product.condition}', '{new_product.sku}', '{new_product.status}', '{new_product.competes_with}', '{new_product.meli_url}', '{new_product.domain_id}', {new_product.seller_id});"
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"Error inserting product: {e}\n on query: {sql}\n with product: {new_product}")
                err = e
        return err
    
    def insertTrackedProduct(self, new_product: Product) -> Exception:
        err:Exception = None
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"INSERT INTO `products` (`meli_id`, `name`, `site_id`, `category_id`, `initial_price`, `secure_thumbnail`, `condition`, `sku`, `status`, `competes_with`, `meli_url`, `domain_id`, `seller_id`, `type`) VALUES ('{new_product.meli_id}', '{new_product.name}', '{new_product.site_id}', '{new_product.category_id}', '{new_product.initial_price}', '{new_product.secure_thumbnail}', '{new_product.condition}', '{new_product.sku}', '{new_product.status}', '{new_product.competes_with}', '{new_product.meli_url}', '{new_product.domain_id}', {new_product.seller_id}, 'tracked');"
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"Error inserting product: {e}\n on query: {sql}\n with product: {new_product}")
                err = e
        return err

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

    def getOurProducts(self) -> List[Product]:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM our_products where `status`!='deleted';") # view for select * from products where seller_id = <shopsi_id>;
            rows = cursor.fetchall()
        our_products = [Product.recreate(**row) for row in rows]
        return our_products

    def getCompetitorProducts(self) -> List[Product]:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM competitors_products where `status`!='deleted';")
            rows = cursor.fetchall()
        
        competitor_products = [Product.recreate(**row) for row in rows]
        return competitor_products

    def getTrackedProducts(self) -> List[Product]:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products where `status`!='deleted' AND `type`='tracked';")
            trackeds = cursor.fetchall()
            
        trackeds = [Product.recreate(**row) for row in trackeds]
        return trackeds

    def getPerformanceReport(self) -> List[Dict]:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM performance") # view for a very complicated query
            return cursor.fetchall()


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
        product:Product = None
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT * FROM `products` WHERE `product_id`='{product_id}';"
            cursor.execute(sql)
            row = cursor.fetchone()
        
        if row:
            product = Product.recreate(**row)
        return product
    
    def getProductCompetitors(self, product_id: str) -> list[Product]:
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT * FROM `products` WHERE `competes_with`=(select `sku` from `products` where `product_id`='{product_id}') and `status`!='deleted';"
            cursor.execute(sql)
            rows = cursor.fetchall()
        
        competitors = []
        for row in rows:
            competitor = Product.recreate(**row)
            competitors.append(competitor)
        
        return competitors