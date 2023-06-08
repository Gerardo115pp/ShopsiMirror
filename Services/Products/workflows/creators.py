""" 
    here we define the workflow for creating new entities, which involves using the meli api, scraping the meli website 
    and using the database. 
"""
import openpyxl as excel
import HttpMessages
import repository
import models
from datetime import datetime

def createProductFromMeliData(item_data: dict, sku:str, is_competitor:bool=False) -> tuple[models.Product, Exception]:
    """ 
        creates a product from meli data, and returns it
        
        item_data definition:
            attributes:str
            condition:str
            free_shipping:str
            id:str //this is the meli_id
            location:str // address
            name:str
            original_price:float|None // dont use this for the initial price field, use base_price from the api response
            price:float // also dont use this, use base_price from the api response
            thumbnail:str
            url:str // this is the meli_url and is/should be the meli api reponse 'permalink' field.
    """
    meli_api_response, err = HttpMessages.meli_api.getMeliItemData(item_data["id"])
    if err:
        return None, err
    
    new_product = models.Product.fromItemData(meli_api_response, sku, is_competitor)
    return new_product, None
    
def createSellerFromId(seller_id: str, meli_oauth: models.MeliAuth) -> tuple[models.Seller, models.SellerReputation,  Exception]:
    """ 
        creates a seller from a meli seller id, and returns it
    """
    seller, reputation, err = HttpMessages.meli_api.getMeliSeller(seller_id, meli_oauth)
    return seller, reputation, err # if error, then getMeliSeller will return None for seller and reputation and the error
    
def createPerformanceReportAsWorkBook(serial:int) -> tuple[excel.Workbook, Exception]:
    err:Exception = None
    
    report_wb: excel.Workbook = excel.Workbook()
    performance_sheet = report_wb.active
    performance_sheet.title = "performance"
    performance_sheet = report_wb["performance"]
    report_rows, err  = repository.performance_records.getPerformanceReportBySerial(serial)
    if err:
        print(f"Error getting performance report: {err}")
        return None, err
    
    performance_sheet['A1'] = "SKU"
    performance_sheet['B1'] = "Nombre"
    performance_sheet['C1'] = "Precio Inicial"
    performance_sheet['D1'] = "URL"
    performance_sheet['E1'] = "Estado"
    performance_sheet['F1'] = "Condición"
    performance_sheet['G1'] = "Propietario"
    performance_sheet['H1'] = "Fecha de medición"
    performance_sheet['I1'] = "Visitas"
    performance_sheet['J1'] = "Ventas"
    performance_sheet['K1'] = "Precio Actual"
    performance_sheet['L1'] = "Inventario"
    performance_sheet['M1'] = "Tiene descuento"
    performance_sheet['N1'] = "ID"
    
    
    
    for h, report_row in enumerate(report_rows):
        performance_sheet[f"A{h+2}"] = report_row.sku
        performance_sheet[f"B{h+2}"] = report_row.name 
        performance_sheet[f"C{h+2}"] = report_row.initial_price 
        performance_sheet[f"D{h+2}"] = "Link"
        performance_sheet[f"D{h+2}"].hyperlink = report_row.meli_url
        performance_sheet[f"E{h+2}"] = report_row.status 
        performance_sheet[f"F{h+2}"] = report_row.condition 
        performance_sheet[f"G{h+2}"] = "Propio" if report_row.is_ours else "Competidor" 
        performance_sheet[f"H{h+2}"] = report_row.recorded
        performance_sheet[f"I{h+2}"] = report_row.visits
        performance_sheet[f"J{h+2}"] = report_row.sales 
        performance_sheet[f"K{h+2}"] = report_row.current_price 
        performance_sheet[f"L{h+2}"] = report_row.stock
        performance_sheet[f"M{h+2}"] = report_row.has_discount
        performance_sheet[f"N{h+2}"] = report_row.meli_id
    
    report_wb.active = performance_sheet
    return report_wb, None

def rapidReportAsWorkBook( rapid_report_rows: list[models.PerformanceReportRow]) -> tuple[excel.Workbook, Exception]:
    err:Exception = None
    report_wb: excel.Workbook = excel.Workbook()
    performance_sheet = report_wb.active
    performance_sheet.title = "performance actual"
    
    performance_sheet['A1'] = "SKU"
    performance_sheet['B1'] = "Nombre"
    performance_sheet['C1'] = "Precio Inicial"
    performance_sheet['D1'] = "URL"
    performance_sheet['E1'] = "Estado"
    performance_sheet['F1'] = "Condición"
    performance_sheet['G1'] = "Propietario"
    performance_sheet['H1'] = "Fecha de medición"
    performance_sheet['I1'] = "Ventas"
    performance_sheet['J1'] = "Precio Actual"
    performance_sheet['K1'] = "Inventario"
    performance_sheet['L1'] = "Tiene descuento"
    performance_sheet['M1'] = "ID"
    
    # rapid_reports only differ from performance reports in that they dont have visits.
    
    try: 
        for h, report_row in enumerate(rapid_report_rows):
            performance_sheet[f"A{h+2}"] = report_row.sku
            performance_sheet[f"B{h+2}"] = report_row.name 
            performance_sheet[f"C{h+2}"] = report_row.initial_price 
            performance_sheet[f"D{h+2}"] = "Link"
            performance_sheet[f"D{h+2}"].hyperlink = report_row.meli_url
            performance_sheet[f"E{h+2}"] = report_row.status 
            performance_sheet[f"F{h+2}"] = report_row.condition 
            performance_sheet[f"G{h+2}"] = "Propio" if report_row.is_ours else "Competidor" 
            performance_sheet[f"H{h+2}"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            performance_sheet[f"I{h+2}"] = report_row.sales
            performance_sheet[f"J{h+2}"] = report_row.current_price 
            performance_sheet[f"K{h+2}"] = report_row.stock 
            performance_sheet[f"L{h+2}"] = report_row.has_discount
            performance_sheet[f"M{h+2}"] = report_row.meli_id
    except Exception as e:
        err = e
    
    report_wb.active = performance_sheet
    return report_wb, err