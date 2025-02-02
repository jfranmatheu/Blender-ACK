from dataclasses import dataclass
from enum import Enum

from bpy.types import Operator, Context


class OpsReturn:
    FINISH = {'FINISHED'}
    CANCEL = {'CANCELLED'}
    PASS = {'PASS_THROUGH'}
    RUN = {'RUNNING_MODAL'}
    UI = {'INTERFACE'}


class SubmodalReturn(Enum):
    STOP = 0        # Stop the submodal
    RUNNING = 1     # Keep running the submodal


def add_modal_handler(operator: Operator, context: Context):
    if not context.window_manager.modal_handler_add(operator):
        print("WARN! Operator failed to add modal handler!")
        return False, OpsReturn.CANCEL
    return True, OpsReturn.RUN
