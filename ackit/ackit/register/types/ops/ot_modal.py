from typing import Set

from bpy.types import Context, Event, UILayout

from .ot_generic import Generic
from ....utils.operator import OpsReturn, add_modal_handler
from ....utils.cursor import OperatorCursorUtils


__all__ = ['Modal']


class Modal(OperatorCursorUtils, Generic):
    modal_finish_keymaps = {}
    modal_cancel_keymaps = {}

    _modal_instance: 'Modal' = None
    _context: Context
    _event: Event

    @classmethod
    def get_modal_instance(cls) -> 'Modal':
        return cls._modal_instance

    ''' Modal Start. '''
    def invoke(self, context: Context, event: Event) -> Set[str]:
        ok, ret = add_modal_handler(self, context)
        if ok:
            self._modal_enter(context, event)
        return ret

    def execute(self, context: Context) -> Set[str]:
        raise NotImplementedError("Call modal via invoke!")

    def _modal_enter(self, context: Context, event: Event) -> None:
        self._context = context
        self._event = event
        self.__class__._modal_instance = self
        self.modal_enter(context, event)

    def modal_enter(self, context: Context, event: Event) -> None:
        pass

    ''' Modal Update. '''
    def modal(self, context: Context, event: Event) -> Set[str]:
        self._context = context
        self._event = event
        ret = self.modal_update(context, event)
        if ret is None:
            return OpsReturn.RUN
        if isinstance(ret, set):
            if ret == OpsReturn.FINISH:
                self._modal_exit(context, cancel=False)
            elif ret == OpsReturn.CANCEL:
                self._modal_exit(context, cancel=True)
            return ret
        return OpsReturn.FINISH

    def modal_update(self, context: Context, event: Event) -> OpsReturn | None:
        pass

    ''' Modal End. '''
    def _modal_exit(self, context: 'Context', cancel: bool) -> None:
        self.restore_cursor(context)
        self.modal_exit(context, cancel)

    def modal_exit(self, context: 'Context', cancel: bool) -> None:
        pass
