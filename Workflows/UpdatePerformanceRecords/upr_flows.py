from prefect import  flow
from datetime import datetime, timedelta
import tasks as upr_tasks
import utils as upr_utils
import Config as upr_config
import repository
import databases
import requests
import schedule
import time
import os

has_schedule_been_printed = False

@flow(name="UpdatePerformanceRecords")
def updatePerformanceRecords():
    incomplete_performance_records = repository.incomplete_performance_records.getCurrentBatch()
    assert len(incomplete_performance_records) > 3, f"len(incomplete_performance_records) is {len(incomplete_performance_records)}, but it should be greater than 3" # testing
    
    current_serial = incomplete_performance_records[0].serial
    
    while not repository.incomplete_performance_records.isBatchComplete(current_serial):
        print(f"Batch {current_serial} is not complete, processing...")
        connection_session:requests.Session = upr_utils.getSession()
        
        for h, ipr in enumerate(incomplete_performance_records):
            print(f"({h+1}/{len(incomplete_performance_records)})::{ipr.meli_id}", end=" - ")
            has_changed = False
            
            assert ipr.meli_url != "no permalink", f"meli_url is 'no permalink' for {ipr.meli_id}"
            
            if not ipr.hasApiData:
                print(f"Updating api data")
                new_ipr, err = upr_tasks.data_recollection.getApiProductData(ipr, connection_session)
                if err is not None:
                    print(f"\nError: {err}")
                    if err == upr_tasks.data_recollection.ProductNotFoundError:
                        print(f"Product {ipr.meli_id} not found, removing from incomplete_performance_records.length({len(incomplete_performance_records)}) - ", end="")
                        incomplete_performance_records.pop(h)
                        print(f"incomplete_performance_records.length({len(incomplete_performance_records)})")
                        
                else:
                    incomplete_performance_records[h] = new_ipr
                    ipr = new_ipr
                    has_changed = True
            
            if not ipr.hasVisitsData:
                print(f"Updating visits")
                try:
                    new_ipr, err = upr_tasks.data_recollection.getVisitsData(ipr, connection_session)
                    if err is not None:
                        print(f"\nError: {err}")
                    else:
                        incomplete_performance_records[h] = new_ipr
                        ipr = new_ipr
                        has_changed = True
                except Exception as e:
                    print(f"\nError: {e}")
                
            if not ipr.hasSalesData:
                print(f"Updating sales")
                new_ipr, err = upr_tasks.data_recollection.getSalesData(ipr)
                if err is not None:
                    print(f"\nError: {err}")
                else:
                    incomplete_performance_records[h] = new_ipr
                    ipr = new_ipr
                    has_changed = True
            
            if has_changed:
                repository.incomplete_performance_records.updateIPR(ipr)
                print(f"{ipr.meli_id} got new data")
                    
            if ipr.isCompleted:
                print(f"Complete")
            
        
        connection_session.close()
        
    has_schedule_been_printed = False
    
@flow(name="UpdateProductStatus")
def updateProductStatus():
    global has_schedule_been_printed
    products = repository.products.getAllProducts()
    upr_tasks.mantainence.updateProductStatus(products)
    has_schedule_been_printed = False
    

repository.incomplete_performance_records.setRepository(databases.createIncompletePerformanceRecordRepository())
repository.performance_records.setRepository(databases.createPerformanceRecordRepository())
repository.products.setRepository(databases.createProductRepository())

schedule.every().friday.at((datetime.now() + timedelta(hours=2, minutes=30)).strftime("%H:%M:%S")).do(updatePerformanceRecords)
schedule.every().day.at((datetime.now() + timedelta(hours=1)).strftime("%H:%M:%S")).do(updateProductStatus)


while True:
    if not has_schedule_been_printed:
        for job in schedule.jobs:
            print(f"\rNext execution: {job.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        has_schedule_been_printed = True

    schedule.run_pending()
    time.sleep(1)
            
            
    
    