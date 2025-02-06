from typing import Tuple, Optional, Union
from bpy import types as bpy_types


__all__ = ['UILayoutDrawer']


class UILayoutDrawer:
    layout: bpy_types.UILayout

    def draw(self, context: bpy_types.Context) -> None:
        self.draw_ui(context, self.layout)
    
    def draw_ui(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> None:
        pass

    def ui_section(self, 
                  layout: bpy_types.UILayout,
                  title: str,
                  icon: Union[str, int] = 'NONE',
                  use_box: bool = True,
                  align: bool = True,
                  direction: str = 'VERTICAL') -> Tuple[bpy_types.UILayout, bpy_types.UILayout]:
        """Create a section with header and content layouts.
        
        Args:
            layout: Parent layout to create section in
            title: Title text for the section header
            icon: Icon identifier (str) or icon_value (int) for the header
            use_box: Whether to wrap header and content in boxes
            align: Whether to align items in the content
            direction: Content layout direction ('VERTICAL' or 'HORIZONTAL')
        
        Returns:
            Tuple of (header_layout, content_layout)
        """
        # Create main column for the section
        section_col = layout.column(align=True)
        
        # Create header
        if use_box:
            header_box = section_col.box()
            header = header_box.row()
        else:
            header = section_col.row()
        
        # Add title with icon or icon_value
        if isinstance(icon, str):
            header.label(text=title, icon=icon)
        else:  # integer icon_value
            header.label(text=title, icon_value=icon)
        
        # Create content area
        if use_box:
            content_box = section_col.box()
            if direction == 'VERTICAL':
                content = content_box.column(align=align)
            else:
                content = content_box.row(align=align)
        else:
            if direction == 'VERTICAL':
                content = section_col.column(align=align)
            else:
                content = section_col.row(align=align)
        
        return header, content
