from typing import Set

from bpy.types import Context, Event, UILayout

from ...operator import OpsReturn
from .generic import Generic


__all__ = ['Action']


class Action(Generic):
    def execute(self, context: Context) -> Set[str]:
        self.action(context)
        return OpsReturn.FINISH

    def action(self, context: 'Context') -> None:
        pass
