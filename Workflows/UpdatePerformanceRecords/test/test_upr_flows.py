from unittest.mock import MagicMock, patch
from prefect import flow
import Config as upr_config
import tasks as upr_tasks
import utils as upr_utils
import repository
import databases
import unittest
import requests
import models


repository.products.setRepository(databases.createProductRepository())

@flow(name="TestApiDataRecollection", validate_parameters=False)
def testApiDataRecollection(performance_data: models.IncompletePerformanceRecord, session:requests.Session=None) -> tuple[models.IncompletePerformanceRecord, Exception]:
    session = session or upr_utils.getSession()
    return upr_tasks.data_recollection.getApiProductData(performance_data, session)

@flow(name="TestVisitsDataRecollection", validate_parameters=False)
def testVisitsDataRecollection(performance_data: models.IncompletePerformanceRecord, session:requests.Session=None) -> tuple[models.IncompletePerformanceRecord, Exception]:
    session = session or upr_utils.getSession()
    return upr_tasks.data_recollection.getVisitsData(performance_data, session)

@flow(name="TestSalesDataRecollection", validate_parameters=False)
def testSalesDataRecollection(performance_data: models.IncompletePerformanceRecord) -> tuple[models.IncompletePerformanceRecord, Exception]:
    return upr_tasks.data_recollection.getSalesData(performance_data)

class TestUpdatePerformanceRecords(unittest.TestCase):
    # def test_live_getApiProductData(self):
    #     active_product = repository.products.getActiveProduct()
        
    #     # Arrange
    #     ipr = models.IncompletePerformanceRecord.create(product_id=active_product.product_id, meli_id=active_product.meli_id, meli_url=active_product.meli_url, serial=1)
    #     session = upr_utils.getSession()
                
    #     # Act
    #     ipr, err = testApiDataRecollection(ipr)
        
    #     # Assert
    #     self.assertIsNone(err)
    #     self.assertIsNotNone(ipr)
    #     self.assertIsNot(ipr.current_price, -1)
    #     self.assertIsNot(ipr.stock, -1)
    #     self.assertIsNot(ipr.has_discounts, False)

    def test_live_getSalesData(self):
        active_product = repository.products.getActiveProduct()
        print(f"testing with active_product: {active_product.meli_id}")
        # Arrange
        ipr = models.IncompletePerformanceRecord.create(product_id=active_product.product_id, meli_id=active_product.meli_id, meli_url=active_product.meli_url, serial=1)
        session = upr_utils.getSession()
                
        # Act
        ipr, err = testSalesDataRecollection(performance_data=ipr)
        
        # Assert
        self.assertIsNone(err)
        self.assertIsNotNone(ipr)
        self.assertIsNot(ipr.sales, -1)
        print(f"sales: {ipr.sales}")
        
    # def test_live_getVisitsData(self):
    #     active_product = repository.products.getActiveProduct()
        
    #     # Arrange
    #     ipr = models.IncompletePerformanceRecord.create(product_id=active_product.product_id, meli_id=active_product.meli_id, meli_url=active_product.meli_url, serial=1)
    #     session = upr_utils.getSession()
                
    #     # Act
    #     ipr, err = testVisitsDataRecollection(performance_data=ipr, session=session)
        
    #     # Assert
    #     self.assertIsNone(err)
    #     self.assertIsNotNone(ipr)
    #     self.assertIsNot(ipr.visits, -1)


if __name__ == "__main__":
    unittest.main()