from . import AuthModels
from . import CategoryModels
from . import SearchModels
from typing import Callable

def _setArgVerifaior(func: Callable) -> None:
    assert callable(func), "Argument must be a function"
    AuthModels.allArgsPresent = func
    CategoryModels.allArgsPresent = func
    SearchModels.allArgsPresent = func
    

