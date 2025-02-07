from enum import Enum, auto
from typing import Callable, Type

from ....types.btypes.ui.menu import Menu
from ....globals import GLOBALS

__all__ = [
    'menu_from_function'
]


def menu_from_function(label: str) -> Type:
    def decorator(func: Callable) -> Type:
        new_cls = Menu.new_from_func(func, label=label)
        return new_cls

    return decorator
