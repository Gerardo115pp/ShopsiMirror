from .mysql_utils import MYSQL_CONFIG, MysqlConnection
from models import Seller, SellerReputation
from datetime import datetime

class SellerDoesntExist(Exception):
    pass

class SellerRepository:
    def __init__(self, config: MYSQL_CONFIG=None) -> None:
        if not config:
            config = MYSQL_CONFIG.createFromEnv()
        self.config:MYSQL_CONFIG = config
    
    def insert(self, seller: Seller, reputation: SellerReputation) -> Exception:
        err:Exception = None
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            datetime_obj = datetime.strptime(seller.meli_registration_date, "%Y-%m-%dT%H:%M:%S.%f%z")
            formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            sql = f"INSERT INTO `sellers` (`seller_id`, `nickname`, `meli_profile_link`, `meli_registration_date`) VALUES ({seller.seller_id}, '{seller.nickname}', '{seller.meli_profile_link}', '{formatted_date}');"
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                err = e
                print(f"{err=}")
                print(f"Error inserting seller: {e}\n on query: {sql}\n with seller: {seller}")
            
            # Insert reputation
            if not err:
                err = self.insertSellerReputation(reputation)
        
        print(f"{err=}")
        return err
    
    def getSellerById(self, seller_id: int) -> tuple[Seller, Exception]:
        seller:Seller = None
        err:Exception = None
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT * FROM `sellers` WHERE `seller_id`={seller_id};"
            try:
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    seller = Seller.recreate(**row)
            except Exception as e:
                print(f"Error getting seller: {e}\n on query: {sql}\n with seller_id: {seller_id}")
                err = e
        return seller, err
       
    def getSellerReputationById(self, seller_id:int) -> tuple[SellerReputation, Exception]:
        reputation:SellerReputation = None
        err:Exception = None
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"SELECT * FROM `sellers_reputation` WHERE `seller_id`={seller_id};"
            try:
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    reputation = SellerReputation.recreate(**row)
                else:
                    err = SellerDoesntExist(f"Seller with id {seller_id} doesn't exist")
            except Exception as e:
                print(f"Error getting seller reputation: {e}\n on query: {sql}\n with seller_id: {seller_id}")
                err = e
        return reputation, err 
    
    def deleteSellerById(self, seller_id: int) -> Exception:
        err:Exception = None
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"DELETE FROM `sellers` WHERE `seller_id`={seller_id};"
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"Error deleting seller: {e}\n on query: {sql}\n with seller_id: {seller_id}")
                err = e
        return err
    
    def insertSellerReputation(self, reputation: SellerReputation) -> Exception:
        err:Exception = None
        with MysqlConnection(self.config) as conn:
            cursor = conn.cursor(dictionary=True)
            sql = f"INSERT INTO `sellers_reputations` (`power_seller_status`, `cancelled_transactions`, `total_transactions`, `positive_ratings`, `negative_ratings`, `neutral_ratings`, `level`, `seller_id`) VALUES ('{reputation.power_seller_status}', {reputation.cancelled_transactions}, {reputation.total_transactions}, {reputation.positive_ratings}, {reputation.negative_ratings}, {reputation.neutral_ratings}, '{reputation.level}', {reputation.seller_id});"
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"Error inserting seller reputation: {e}\n on query: {sql}\n with reputation: {reputation}")
                err = e
        return err
    
    
    
    
    