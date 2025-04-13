from typing import Set, Callable, ClassVar

from bpy.types import Context, Event, UILayout, Operator, OperatorProperties

from ...core.base_type import BaseType
from ...enums.operator import OpsReturn

__all__ = ['Generic']


class Generic(BaseType, Operator):
    bl_idname: str
    bl_label: str
    bl_description: str
    bl_options: Set[str]
    bl_cursor_pending: str  # when using 'DEPENDS_ON_CURSOR' in bl_options.

    # Explicitly declare _polling_functions as required by the Pollable protocol
    # Use ClassVar because it's initialized at the class level
    _polling_functions: ClassVar[Set[Callable[[Context], bool]]] = set()

    @classmethod
    def run(cls, **operator_properties: dict) -> None:
        eval("bpy.ops." + cls.bl_idname)(**operator_properties)

    @classmethod
    def run_invoke(cls, **operator_properties: dict) -> None:
        eval("bpy.ops." + cls.bl_idname)("INVOKE_DEFAULT", **operator_properties)

    @classmethod
    def draw_in_layout(
        cls,
        layout: UILayout,
        text: str | None = None,
        icon: str | int | None = None,
        depress: bool = False,
        emboss: bool = False,
        op_props: dict | None = None,
        **draw_kwargs: dict,
    ) -> OperatorProperties:
        op_text = text if text is not None else cls.bl_label
        op_icon_str = icon if isinstance(icon, str) else "NONE"
        op_icon_val = icon if isinstance(icon, int) else 0

        op = layout.operator(
            cls.bl_idname,
            text=op_text,
            icon=op_icon_str,
            icon_value=op_icon_val,
            depress=depress,
            emboss=emboss,
            **draw_kwargs
        )
        if op_props:
            for key, value in op_props.items():
                setattr(op, key, value)
        return op

    @classmethod
    def poll(cls, context: Context) -> bool:
        if cls._polling_functions:
            for func in cls._polling_functions:
                if not func(context):
                    return False
        return True

    def invoke(self, context: Context, event: Event) -> Set[str]:
        return self.execute(context)

    def execute(self, context: Context) -> Set[str]:
        return OpsReturn.FINISH

    def modal(self, context: Context, event: Event) -> Set[str]:
        return OpsReturn.FINISH


    ''' Report. '''
    def report_debug(self, message: str) -> None:
        self.report({"DEBUG"}, message)

    def report_info(self, message: str) -> None:
        self.report({"INFO"}, message)

    def report_warning(self, message: str) -> None:
        self.report({"WARNING"}, message)

    def report_error(self, message: str) -> Set[str]:
        self.report({"ERROR"}, message)
        return OpsReturn.CANCEL

    def report_error_invalid_context(self, message: str = "Invalid Context") -> Set[str]:
        self.report({"ERROR_INVALID_CONTEXT"}, message)
        return OpsReturn.CANCEL

    def report_error_invalid_input(self, message: str = "Invalid Input") -> Set[str]:
        self.report({"ERROR_INVALID_INPUT"}, message)
        return OpsReturn.CANCEL
