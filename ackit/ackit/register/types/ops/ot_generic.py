from typing import Set

from bpy.types import Context, Event, UILayout, Operator

from ....utils.operator import OpsReturn
from ..base import BaseType
from ..props.layout import DescriptorProps_PropsTuple, DescriptorProps_Props, DescriptorProps_DrawProps, DescriptorProps_DrawUILayout
from ..props.descriptors import BlenderPropertyDescriptor


__all__ = ['Generic']


class Generic(DescriptorProps_PropsTuple, BaseType):
    bl_idname: str
    bl_label: str
    bl_description: str
    bl_options: Set[str]
    bl_cursor_pending: str  # when using 'DEPENDS_ON_CURSOR' in bl_options.

    # Polling functions added via Polling decorators utility.
    _polling_functions: Set[callable] | None = None

    @classmethod
    def tag_register(cls):
        new_cls = super().tag_register(Operator, 'OT')

        # Ensure annotations exist
        if not hasattr(new_cls, '__annotations__'):
            new_cls.__annotations__ = {}

        # Manually initialize descriptors
        # to FIX self.props.{prop_name} accesor.
        for name, value in cls.__dict__.items():
            if isinstance(value, BlenderPropertyDescriptor):
                # Create a new copy of the descriptor
                new_descriptor = value.copy()
                new_descriptor.initialize(new_cls, name)
                setattr(new_cls, name, new_descriptor)

        return new_cls

    @classmethod
    def poll(cls, context: Context) -> bool:
        if cls._polling_functions:
            for func in cls._polling_functions:
                if not func(context):
                    return False
        return True

    def draw(self, context):
        self.draw_ui(context, self.layout)

    def draw_ui(self, context: Context, layout: UILayout) -> None:
        pass

    def invoke(self, context: Context, event: Event) -> Set[str]:
        return self.execute(context)

    def execute(self, context: Context, event: Event) -> Set[str]:
        return OpsReturn.FINISH

    def modal(self, context: Context, event: Event) -> Set[str]:
        return OpsReturn.FINISH
