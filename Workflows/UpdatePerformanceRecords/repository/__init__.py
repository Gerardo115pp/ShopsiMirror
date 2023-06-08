from . import incomplete_performance_records
from . import performance_records
from . import products
from typing import Any

def _checkMethodImplemented(cls: Any, method_name: str) -> bool:
    return hasattr(cls, method_name) and (callable(getattr(cls, method_name)) or isinstance(getattr(cls, method_name), property))

incomplete_performance_records.checkMethodImplemented = _checkMethodImplemented
performance_records.checkMethodImplemented = _checkMethodImplemented
products.checkMethodImplemented = _checkMethodImplemented
