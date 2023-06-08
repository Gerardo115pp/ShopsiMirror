from . import IncompletePerformanceRecord as ipr_module
from . import PerformanceRecord as pr_module
from . import Product as product_module
from inspect import getfullargspec
from typing import List

def _allArgsPresent(obj: object, args: List[str]) -> bool:
    all_args = getfullargspec(obj).args
    are_all_present =  all(arg in all_args or arg == "self" for arg in args)
    if not are_all_present:
        print(f"({args}) are not all present in ({all_args})")
        
    return are_all_present

# We import all the classes from the module here to make them available to the rest of the package without having to import the module itself

ipr_module.allArgsPresent = _allArgsPresent
IncompletePerformanceRecord = ipr_module.IncompletePerformanceRecord

pr_module.allArgsPresent = _allArgsPresent
PerformanceRecord = pr_module.PerformanceRecord

product_module.allArgsPresent = _allArgsPresent
Product = product_module.Product

