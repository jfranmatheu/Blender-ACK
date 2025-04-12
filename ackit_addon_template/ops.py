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
