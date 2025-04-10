from typing import Any, Tuple, Optional, ClassVar
from bpy.types import UILayout, OperatorProperties
import bpy

# Auto-generated operator classes
# DO NOT EDIT MANUALLY

class __base_op:
    bl_idname: ClassVar[str]

    @classmethod
    def draw_in_layout(
        cls,
        layout: UILayout,
        text: Optional[str] = '',
        icon: Optional[str | int] = 'NONE',
        depress: bool = False,
        emboss: bool = False,
        op_props: Optional[dict] = None,
        **draw_kwargs: dict,
    ) -> OperatorProperties:
        """Draw operator in the given layout.

        Args:
            layout (UILayout): The layout to draw in
            text (Optional[str], optional): Button text. Defaults to an empty string.
            icon (Optional[str | int], optional): Button icon. Defaults to 'NONE'.
            depress (bool, optional): Draw button as pressed. Defaults to False.
            emboss (bool, optional): Draw button embossed. Defaults to False.
            op_props (Optional[dict], optional): Operator properties. Defaults to None.
            **draw_kwargs: Additional keyword arguments for layout.operator()

        Returns:
            OperatorProperties: The operator properties
        """
        op = layout.operator(
            cls.bl_idname,
            text=text,
            icon=icon if isinstance(icon, str) else 'NONE',
            icon_value=icon if isinstance(icon, int) else 0,
            depress=depress,
            emboss=emboss,
            **draw_kwargs
        )
        if op_props:
            for key, value in op_props.items():
                setattr(op, key, value)
        return op


class ACKITADDONTEMPLATE_OT_Action_Operator(__base_op):
    """
    Test Action

    Transforms active mesh object location in Z axis
    """
    bl_idname: ClassVar[str] = 'ackitaddontemplate.action_operator'

    @classmethod
    def run(
        cls,
        *,  # Force keyword arguments
        enable: Optional[bool] = None,
        z_location: Optional[float] = None,
    ) -> None:
        """Execute the Test Action operator.

        Args:
        - `enable` (bool): 
        - `z_location` (float): 
        """
        props = {
            'enable': enable if enable is not None else None,
            'z_location': z_location if z_location is not None else None,
        }
        # Filter out None values
        props = {k: v for k, v in props.items() if v is not None}
        bpy.ops.ackitaddontemplate.action_operator(**props)

    @classmethod
    def run_invoke(
        cls,
        *,  # Force keyword arguments
        enable: Optional[bool] = None,
        z_location: Optional[float] = None,
    ) -> None:
        """Execute the Test Action operator in INVOKE_DEFAULT mode.

        This mode shows the operator's UI if it has one.

        Args:
        - `enable` (bool): 
        - `z_location` (float): 
        """
        props = {
            'enable': enable if enable is not None else None,
            'z_location': z_location if z_location is not None else None,
        }
        # Filter out None values
        props = {k: v for k, v in props.items() if v is not None}
        bpy.ops.ackitaddontemplate.action_operator('INVOKE_DEFAULT', **props)


class ACKITADDONTEMPLATE_OT_Modal_Draw_Operator(__base_op):
    """
    Modal Draw Operator


    """
    bl_idname: ClassVar[str] = 'ackitaddontemplate.modal_draw_operator'

    @classmethod
    def run(
        cls,
        # No properties.
    ) -> None:
        """Execute the Modal Draw Operator operator.

        Args:
        """
        props = {
        }
        # Filter out None values
        props = {k: v for k, v in props.items() if v is not None}
        bpy.ops.ackitaddontemplate.modal_draw_operator(**props)

    @classmethod
    def run_invoke(
        cls,
        # No properties
    ) -> None:
        """Execute the Modal Draw Operator operator in INVOKE_DEFAULT mode.

        This mode shows the operator's UI if it has one.

        Args:
        """
        props = {
        }
        # Filter out None values
        props = {k: v for k, v in props.items() if v is not None}
        bpy.ops.ackitaddontemplate.modal_draw_operator('INVOKE_DEFAULT', **props)


class ACKITADDONTEMPLATE_OT_Generic_Operator(__base_op):
    """
    Generic Operator


    """
    bl_idname: ClassVar[str] = 'ackitaddontemplate.generic_operator'

    @classmethod
    def run(
        cls,
        *,  # Force keyword arguments
        new_name: Optional[str] = 'Best Name Ever',
    ) -> None:
        """Execute the Generic Operator operator.

        Args:
        - `new_name` (str): 
        """
        props = {
            'new_name': new_name if new_name is not None else None,
        }
        # Filter out None values
        props = {k: v for k, v in props.items() if v is not None}
        bpy.ops.ackitaddontemplate.generic_operator(**props)

    @classmethod
    def run_invoke(
        cls,
        *,  # Force keyword arguments
        new_name: Optional[str] = 'Best Name Ever',
    ) -> None:
        """Execute the Generic Operator operator in INVOKE_DEFAULT mode.

        This mode shows the operator's UI if it has one.

        Args:
        - `new_name` (str): 
        """
        props = {
            'new_name': new_name if new_name is not None else None,
        }
        # Filter out None values
        props = {k: v for k, v in props.items() if v is not None}
        bpy.ops.ackitaddontemplate.generic_operator('INVOKE_DEFAULT', **props)
