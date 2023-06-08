from flask import Blueprint, request, make_response, current_app, jsonify
from openpyxl.writer.excel import save_virtual_workbook 
from flask_sock import Sock, Server as SockServer
from middleware.auth import token_required
from datetime import datetime, timedelta
import Config as service_config
import openpyxl as excel
from uuid import uuid4
from threading import Thread, Timer
import repository
import workflows
import models
import json
import time


reports_blueprint = Blueprint('reports', __name__)
reports_sock = Sock(reports_blueprint)

rapid_reports_cache = {}



@reports_blueprint.route('/list', methods=['GET'])
@token_required
def getReportsList(user_data: dict[str, str]):
    err: Exception = None
    reports: models.Reports = None
    
    reports, err = repository.performance_records.getReportsList()
    print(f"reports: {reports.reports}")
    if err:
        print(f"error while getting reports list: {err}")
        return make_response(jsonify({"error": "error while getting reports list"}), 500)
    
    return jsonify(reports.toDict())

@reports_blueprint.route('/excel', methods=['GET'])
@token_required
def handleGetExcelBySerial(user_data: dict[str, str]):
    serial = request.args.get('serial')
    if not serial:
        print(f"no serial provided")
        return make_response(jsonify({"error": "no serial provided"}), 400)
    
    err: Exception = None
    performance_report: excel.Workbook = None
    
    performance_report, err = workflows.creators.createPerformanceReportAsWorkBook(serial)
    if err:
        return make_response(jsonify({"error": f"report with serial number {serial}, doesnt exists"}), 404)
    
    virtual_workbook = save_virtual_workbook(performance_report)
    filename = f"tracked-products-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.xlsx"
    
    response = make_response(virtual_workbook)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
    return response
    
@reports_sock.route('/rapid-report')
def rapidReport(ws: SockServer):
    """ 
        create a rapid report, this means updateing the status of all product,
        retrive the ones with active status after update, and extract the data of a performance record with the exception of visits
    """
    err: Exception = None
    
    ws.send(json.dumps({
        "type": "report_started",
        "human_message": "Iniciando reporte rapido"
    }))
    all_products = repository.products.getAllProducts()
    ws.send(json.dumps({
        "type": "stage_changed",
        "human_message": f"Actualizando estado de {len(all_products)} productos"
    }))
    
    err = workflows.collectors.updateProductStatus(all_products)
    if err:
        ws.send(json.dumps({"type": "error", "error": f"error while updating products status: {err}"}))
        ws.close(1000, 'cant update products status')
        return
    # DEBUG: use sleep to simulate a long process in case of testing
    # time.sleep(0.5) # simulate update time
    
    active_products = repository.products.getActiveProducts() # updateProductStatus() updates the status of all products 
    limiter = 1  # a len(active_products) / limiter, used for debuging
    rapid_report_records: list[models.PerformanceReportRow] = [] 
    
    print(f"active products: {len(active_products)}")
    ws.send(json.dumps({
        "type": "stage_changed",
        "human_message": f"Obteniendo datos de {len(active_products)} productos",
        "length": len(active_products)//limiter,
        "progress": 0
    }))
    
    # GET PARCIAL PERFORMANCE RECORDS
    product_data_session: workflows.collectors.http_messages.Session = None
    sales_data_session: workflows.collectors.http_messages.Session = None
       
    for h, product in enumerate(active_products[:len(active_products)//limiter]):
        rapid_performance_record = models.IncompletePerformanceRecord(product.product_id, 1, product.meli_id, product.meli_url)
        print(f"product: {rapid_performance_record.meli_id}")
        if rapid_performance_record.meli_url == "no permalink":
            print(f"product {rapid_performance_record.meli_id} has no permalink")
            ws.send(json.dumps({
                "type": "progress_made",
                "human_message": f"Saltando de {rapid_performance_record.meli_id}",
                "length": len(active_products)//limiter,
                "progress": h + 1
            }))
            continue
        
        rapid_performance_record, err, product_data_session = workflows.collectors.getApiProductData(rapid_performance_record, product_data_session)
        if err:
            print(f"error while getting product data: {err}")
            continue
        
        rapid_performance_record, err, sales_data_session = workflows.collectors.getSalesData(rapid_performance_record, sales_data_session)
        if err:
            print(f"error while getting sales data: {err}")
            continue
            
        print(f"everything!: {rapid_performance_record}")
        if rapid_performance_record.hasApiData and rapid_performance_record.hasSalesData:
            rapid_report_row: models.PerformanceReportRow = models.PerformanceReportRow(product.name, product.initial_price, product.condition, product.sku, product.status, product.competes_with == "", product.meli_url, product.meli_id, datetime.now(), 0, rapid_performance_record.sales, rapid_performance_record.current_price, rapid_performance_record.stock, rapid_performance_record.has_discounts)
            rapid_report_records.append(rapid_report_row)
            
        ws.send(json.dumps({
            "type": "progress_made",
            "human_message": f"Obteniendo datos de {rapid_performance_record.meli_id}",
            "length": len(active_products)//limiter,
            "progress": h + 1
        }))
        # time.sleep(0.2) # simulate update time
    
    print(f"Creating report workbook with {len(rapid_report_records)} rows")
    rapid_report: excel.Workbook = None
    rapid_report, err = workflows.creators.rapidReportAsWorkBook(rapid_report_records)
    if err:
        print(f"error while creating rapid report: {err}")
        ws.send(json.dumps({"type": "error", "error": f"error while creating rapid report: {err}"}))
        ws.close(1000, 'cant create rapid report')
        return
    
    # UNCOMMENT TO TEST
    # repid_report: excel.Workbook = excel.Workbook()
    # report_sheet = repid_report.active
    # report_sheet.title = f"rapid-report-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    
    # # fill report sheet with random data, this is just a simulation
    # report_sheet.append(["product", "product name", "product category", "product price", "product quantity", "product status"])
    # report_sheet.append(["product-1", "product name 1", "product category 1", "product price 1", "product quantity 1", "product status 1"])
    
    virtual_workbook = save_virtual_workbook(rapid_report)
    rapid_report_id = str(uuid4())
    
    rapid_reports_cache[rapid_report_id] = virtual_workbook
    ws.send(json.dumps({
        "type": "report_finished",
        "human_message": "report finished.",
        "report_id": rapid_report_id
    }))
    
    ws.close(1000, 'report finished')    
    
@reports_blueprint.route('/rapid-report-download', methods=['GET'])
@token_required
def downloadRapidReport(user_data: dict[str, str]):
    report_id = request.args.get('report_id')
    if not report_id:
        return make_response(jsonify({"error": "no report id provided"}), 400)
    
    if report_id not in rapid_reports_cache:
        return make_response(jsonify({"error": "report id doesnt exists"}), 404)
    
    virtual_workbook = rapid_reports_cache[report_id]
    filename = f"rapid-report-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.xlsx"
    
    response = make_response(virtual_workbook)
    
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
    
    creator = user_data.get('username', 'unknown')
    workflows.notifiers.emitRapidReportCreated(creator, f"'{creator}' created a rapid report")
    
    def freeReportMemory(report_id: str):
        del rapid_reports_cache[report_id]
        print(f"report {report_id} deleted from cache")
    
    garbage_collector = Timer(0.7, freeReportMemory, kwargs={"report_id": report_id})
    garbage_collector.start()
    
    return response
