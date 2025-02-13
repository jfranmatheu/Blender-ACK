import re
from typing import Type, List

import bpy

from ...globals import GLOBALS
from ...debug.output import print_debug
from ..utils import get_subclasses_recursive
from ..btypes import BTypes

__all__ = [
    'BaseType'
]


class BaseType(object):
    original_name: str
    original_cls: Type
    registered: bool = False

    @classmethod
    def __subclasses_recursive__(cls) -> List['BaseType']:
        return get_subclasses_recursive(cls, only_outermost=True)

    @classmethod
    def tag_register(cls, bpy_type: type | str, type_key: str | None, *subtypes, **kwargs):
        if 'from_function' in kwargs:
            from_function = kwargs.pop('from_function')
            original_cls = from_function
            original_cls_name = from_function.__name__
            original_cls_module = from_function.__module__
        else:
            from_function = None
            original_cls = cls
            original_cls_name = cls.__name__
            original_cls_module = cls.__module__
        
        if hasattr(original_cls, 'registered') and original_cls.registered:
            return cls

        if isinstance(bpy_type, str):
            bpy_type = getattr(bpy.types, bpy_type)

        print_debug(f"--> Tag-Register class '{original_cls_name}' of type '{bpy_type.__name__} (from fn? {from_function is not None}) --> Package: {original_cls_module}'")

        # Modify/Extend original class.
        if type_key is not None:
            # Identify the words at the original class name,
            # useful to create unique identifiers in the correct naming convention.
            pattern = r'[A-Z][a-z0-9]*|[a-zA-Z0-9]+'
            keywords = re.findall(pattern, original_cls_name)
            idname: str = '_'.join([word.lower() for word in keywords])

            # CLass name if a bpy-type key is specified. (eg. UL, PT, MT, OT, GZ, GZG, etc.)
            cls_name = f'{GLOBALS.ADDON_MODULE_UPPER}_{type_key}_{idname}'

            print("\t- cls_name:", cls_name)

            # Check if the original class has specified a label and description/tooltip attributes.
            if not hasattr(cls, 'bl_label') or not cls.bl_label:
                kwargs['bl_label'] = cls.label if hasattr(cls, 'label') else ' '.join(keywords)
            if not hasattr(cls, 'bl_description') or not cls.bl_label:
                kwargs['bl_description'] = cls.tooltip if hasattr(cls, 'tooltip') else cls.description if hasattr(cls, 'description') else ''

            # Some bpy types may require a bl_idname.
            if bpy_type == bpy.types.Operator:
                # Operator types idname should have an specific naming convention.
                kwargs['bl_idname'] = f"{GLOBALS.ADDON_MODULE_SHORT.lower()}.{idname}"

            elif bpy_type in {bpy.types.Menu, bpy.types.Panel, bpy.types.UIList}:
                # In the case of interface bpy.types, we can re-use the class name for the idname.
                kwargs['bl_idname'] = cls_name
        else:
            if bpy_type == bpy.types.AddonPreferences:
                # We override the original's class name for a name convention one.
                cls_name = f'{GLOBALS.ADDON_MODULE_UPPER}_AddonPreferences'
                kwargs['bl_idname'] = GLOBALS.ADDON_MODULE
            else:
                # This case is for unhandled bpy_types. We re-use the original's class name.
                cls_name = original_cls_name # f'{GLOBALS.ADDON_MODULE_UPPER}_{idname}'

        # Preserve original class data.
        kwargs['original_name'] = original_cls_name
        kwargs['original_cls'] = original_cls

        # Mark as registered, same for newly created type (based on bpy_types).
        original_cls.registered = True
        kwargs['registered'] = True

        # Create new Blender type to be registered.
        new_cls = type(
            cls_name,
            (cls, *subtypes, bpy_type),
            kwargs
        )

        # Preserve original module to avoid issues excluding new classes due to being inside of '/types' directory!
        new_cls.__module__ = original_cls_module

        # Add this new class to be registered as a new BType (Blender type).
        btype: BTypes = getattr(BTypes, bpy_type.__name__)
        btype.add_class(new_cls)

        return new_cls


# ----------------------------------------------------------------

def init():
    for subcls in BaseType.__subclasses_recursive__():
        if 'types' in subcls.__module__:
           # SKIP: IF THE SUBCLASS IS INSIDE THE addon_utils module or inside any folder called 'types'.
           continue
        subcls.tag_register()
