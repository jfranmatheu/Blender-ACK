from bpy import types as bpy_types

from ..base_type import BaseType
from ....utils.previews import get_preview_id_from_image_path
from ....globals import GLOBALS

__all__ = ['AddonPreferences']


class AddonPreferences(BaseType):
    _bpy_type = bpy_types.AddonPreferences

    logo_scale: int = 10

    @classmethod
    def get_prefs(cls, context: bpy_types.Context) -> bpy_types.AddonPreferences:
        return context.preferences.addons[cls.bl_idname].preferences
    
    def draw(self, context: bpy_types.Context) -> None:
        layout: bpy_types.UILayout = self.layout

        # DRAW LOGO.
        # ----------------------------------------------------------------

        def _get_logo_icon_id() -> int:
            image_path = GLOBALS.IMAGES_PATH / 'prefs-logo.png'
            if not image_path.exists():
                image_path = GLOBALS.IMAGES_PATH / 'prefs-logo.jpg'
            if not image_path.exists():
                return 0
            return get_preview_id_from_image_path(str(image_path))

        if icon_id :=_get_logo_icon_id():
            row = layout.row(align=True)
            row.scale_y = 0.5
            row.template_icon(icon_value=icon_id, scale=self.logo_scale)

        super().draw(context)
