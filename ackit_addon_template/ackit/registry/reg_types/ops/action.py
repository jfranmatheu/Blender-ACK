from typing import Set, Callable

from bpy.types import Context, Event, UILayout

from ....enums.operator import OpsReturn
from .generic import Generic


__all__ = ['Action']


class Action(Generic):

    @classmethod
    def from_function(cls, label: str, **kwargs) -> 'Action':
        def decorator(func: Callable) -> 'Action':
            new_cls = type(
                func.__name__,
                (Action, ),
                {
                    **kwargs,
                    'label': label,
                    'action': func,
                }
            )
            new_cls.__module__ = func.__module__
            new_cls.tag_register()
            return new_cls
        return decorator

    def execute(self, context: Context) -> Set[str]:
        self.action(context)
        return OpsReturn.FINISH

    def action(self, context: 'Context') -> None:
        pass
