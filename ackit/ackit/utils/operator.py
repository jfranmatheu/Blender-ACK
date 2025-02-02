from dataclasses import dataclass


class OpsReturn:
    FINISH = {'FINISHED'}
    CANCEL = {'CANCELLED'}
    PASS = {'PASS_THROUGH'}
    RUN = {'RUNNING_MODAL'}
    UI = {'INTERFACE'}


def add_modal_handler(operator, context):
    if not context.window_manager.modal_handler_add(operator):
        print("WARN! Operator failed to add modal handler!")
        return False, OpsReturn.CANCEL
    return True, OpsReturn.RUN
