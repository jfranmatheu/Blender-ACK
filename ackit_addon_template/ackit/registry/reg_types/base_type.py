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


type_key_per_bpy_type = {
    bpy.types.Operator: 'OT',
    bpy.types.Panel: 'PT',
    bpy.types.Menu: 'MT',
    bpy.types.UIList: 'UL',
    bpy.types.Gizmo: 'GZ',
    bpy.types.GizmoGroup: 'GZG',
    bpy.types.Node: 'ND',
    bpy.types.NodeSocket: 'NDSK',
    bpy.types.NodeTreeInterfaceSocket: 'NTISK',
    bpy.types.NodeTree: 'NT',
    bpy.types.AddonPreferences: 'AP',
}


class BaseType(object):
    original_name: str
    original_cls: Type
    registered: bool = False

    @classmethod
    def __subclasses_recursive__(cls) -> List['BaseType']:
        return get_subclasses_recursive(cls, only_outermost=True)
    
    @classmethod
    def get_bpy_type(cls) -> Type:
        for cls in cls.__mro__:
            if cls in type_key_per_bpy_type:
                return cls
        raise ValueError(f"No bpy.types found in MRO of {cls.__name__}")

    @classmethod
    def get_idname(cls) -> str:
        if hasattr(cls, 'bl_idname') and cls.bl_idname:
            return cls.bl_idname

        bpy_type = cls.get_bpy_type()
        type_key = type_key_per_bpy_type.get(bpy_type, None)

        if type_key is None:
            return cls.__name__
        if bpy_type == bpy.types.AddonPreferences:
            return f"{GLOBALS.ADDON_MODULE_UPPER}_AddonPreferences"

        # Identify the words at the original class name,
        # useful to create unique identifiers in the correct naming convention.
        pattern = r'[A-Z][a-z0-9]*|[a-zA-Z0-9]+'
        keywords = re.findall(pattern, cls.__name__)
        idname: str = '_'.join([word.lower() for word in keywords])

        if bpy_type == bpy.types.Operator:
            return f"{GLOBALS.ADDON_MODULE_UPPER.lower()}.{idname}"

        return f"{GLOBALS.ADDON_MODULE_UPPER}_{type_key}_{idname}"

    @classmethod
    def tag_register(cls, *subtypes, **kwargs):
        bpy_type = cls.get_bpy_type()
        type_key = type_key_per_bpy_type.get(bpy_type, None)

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

        kwargs['bl_idname'] = cls.get_idname()

        # Modify/Extend original class.
        if bpy_type == bpy.types.AddonPreferences:
            # We override the original's class name for a name convention one.
            cls_name = f'{GLOBALS.ADDON_MODULE_UPPER}_AddonPreferences'
        elif type_key is not None:
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
        else:
            # This case is for unhandled bpy_types. We re-use the original's class name.
            cls_name = original_cls_name # f'{GLOBALS.ADDON_MODULE_UPPER}_{idname}'

        # Preserve original class data.
        kwargs['original_name'] = original_cls_name
        kwargs['original_cls'] = original_cls

        # Mark as registered, same for newly created type (based on bpy_types).
        original_cls.registered = True
        kwargs['registered'] = True

        def create_new_cls():
            # Create new class.
            if len(subtypes) == 0:
                # for key, value in kwargs.items():
                #     setattr(cls, key, value)
                # return cls
                # NOTE: we don't need to create a new class, we can use the original one.
                # BUT, since it might be possible to have wrapped properties in the original class,
                # we need to create a new class to avoid issues with the annotations.
                _subtypes = (cls,)
            else:
                _subtypes = (cls, *subtypes)

            # Create new Blender type
            new_cls = type(
                cls_name,
                _subtypes,
                kwargs
            )
            # Preserve original module to avoid issues excluding new classes due to being inside of '/types' directory!
            new_cls.__module__ = original_cls_module

            # Handle wrapped properties in annotations
            if hasattr(original_cls, '__annotations__'):
                if not hasattr(new_cls, '__annotations__'):
                    new_cls.__annotations__ = {}

                for name, value in original_cls.__annotations__.items():
                    if hasattr(value, 'create_property'):
                        # Create actual property from wrapped property
                        new_cls.__annotations__[name] = value.create_property(new_cls)
                    elif name not in new_cls.__annotations__:
                        # Keep non-wrapped properties as is
                        new_cls.__annotations__[name] = value

            return new_cls

        new_cls = create_new_cls()

        # Add to BTypes registry
        btype: BTypes = getattr(BTypes, bpy_type.__name__)
        btype.add_class(new_cls)

        return new_cls


# ----------------------------------------------------------------

def init():
    for subcls in BaseType.__subclasses_recursive__():
        if 'reg_types' in subcls.__module__:
           # SKIP: IF THE SUBCLASS IS INSIDE THE addon_utils module or inside any folder called 'reg_types'.
           continue
        subcls.tag_register()
