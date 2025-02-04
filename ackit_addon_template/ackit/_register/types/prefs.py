from bpy import types as bpy_types

from .base import BaseType
from .layout import Layout


__all__ = ['AddonPreferences']


class AddonPreferences(BaseType, Layout):

    @classmethod
    def tag_register(cls, *subtypes, **kwargs):
        return super().tag_register(bpy_types.AddonPreferences, None, *subtypes, **kwargs)

    @classmethod
    def get_prefs(cls, context: bpy_types.Context) -> bpy_types.AddonPreferences:
        return context.preferences.addons[cls.bl_idname].preferences
