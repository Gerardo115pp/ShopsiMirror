from . import IncompletePerformanceRecord as ipr_module
from . import PerformanceRecord as pr_module
from . import Product as product_module
from . import Seller as seller_module
from . import MeliModels as mi_module
from . import Reports as reports_module
from . import SystemEvents as se_module
from inspect import getfullargspec
from typing import List

def _allArgsPresent(obj: object, args: List[str]) -> bool:
    all_args = getfullargspec(obj).args
    are_all_present = True
    for arg in all_args:
        if arg not in args and arg != "self":
            print(f"Missing argument: {arg} in {obj.__name__}")
            are_all_present = False
            break
        
    return are_all_present

# We import all the classes from the module here to make them available to the rest of the package without having to import the module itself

ipr_module.allArgsPresent = _allArgsPresent
IncompletePerformanceRecord = ipr_module.IncompletePerformanceRecord

pr_module.allArgsPresent = _allArgsPresent
PerformanceRecord = pr_module.PerformanceRecord

product_module.allArgsPresent = _allArgsPresent
Product = product_module.Product
OurProduct = product_module.OurProduct
CustomQuery = product_module.CustomQuery


seller_module.allArgsPresent = _allArgsPresent
Seller = seller_module.Seller
SellerReputation = seller_module.SellerReputation

reports_module.allArgsPresent = _allArgsPresent
PerformanceReportRow = reports_module.PerformanceReportRow
ReportData = reports_module.ReportData
Reports = reports_module.Reports

mi_module._setArgVerifaior(_allArgsPresent)
assert mi_module.SearchModels.allArgsPresent is _allArgsPresent, "Something went wrong"
MeliItem = mi_module.SearchModels.MeliItem
MeliSearchResults = mi_module.SearchModels.MeliSearchResults
MeliAuth = mi_module.AuthModels.MeliAuth
CategoryData = mi_module.CategoryModels.CategoryData
CategoryRedux = mi_module.CategoryModels.CategoryRedux
Trend = mi_module.CategoryModels.Trend
CategoryTrends = mi_module.CategoryModels.CategoryTrends


SystemEvent = se_module.SystemEvent
event_types = se_module.EventTypes

