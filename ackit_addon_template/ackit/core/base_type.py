import re
from typing import Type, List

import bpy

from ..globals import GLOBALS
from ..debug.output import print_debug
from .reg_utils import get_subclasses_recursive
from .btypes import BTypes


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
    bl_idname: str
    bl_label: str
    bl_description: str

    original_name: str
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
    def tag_register(cls, **kwargs):
        # Check if already registered
        if hasattr(cls, 'registered') and cls.registered:
            return cls
        
        bpy_type = cls.get_bpy_type()
        type_key = type_key_per_bpy_type.get(bpy_type, None)

        # Store original name for reference
        original_name = cls.__name__

        # Set the bl_idname
        idname = cls.get_idname()
        setattr(cls, 'bl_idname', idname)

        # Set required Blender attributes based on type
        if bpy_type == bpy.types.AddonPreferences:
            # AddonPreferences doesn't need additional attributes
            new_cls_name = f'{GLOBALS.ADDON_MODULE_UPPER}_AddonPreferences'
        elif type_key is not None:
            # Identify the words in the class name for label generation
            pattern = r'[A-Z][a-z0-9]*|[a-zA-Z0-9]+'
            keywords = re.findall(pattern, original_name)  # Use original name for label generation
            
            # Set bl_label if not already set
            if not hasattr(cls, 'bl_label') or not cls.bl_label:
                setattr(cls, 'bl_label', cls.label if hasattr(cls, 'label') else ' '.join(keywords))
            
            # Set bl_description if not already set
            if not hasattr(cls, 'bl_description') or not cls.bl_description:
                description = cls.tooltip if hasattr(cls, 'tooltip') else cls.description if hasattr(cls, 'description') else ''
                setattr(cls, 'bl_description', description)

            # Construct class name with addon prefix and type key
            cls_name_sufix = '_'.join(keywords)
            new_cls_name = f'{GLOBALS.ADDON_MODULE_UPPER}_{type_key}_{cls_name_sufix}'
        else:
            new_cls_name = original_name

        # Apply the new name to the original class
        cls.__name__ = new_cls_name

        # Store original name in the class (like in the original implementation)
        setattr(cls, 'original_name', original_name)

        # Mark as registered
        cls.registered = True

        # Handle wrapped properties (Descriptors).
        for name, value in cls.__dict__.items():
            # WrappedPropertyDescriptor.
            if hasattr(value, 'create_property'):
                value.create_property(name, cls)

        if isinstance(cls, bpy.types.Node):
            for name, value in cls.__dict__.items():
                # NodeSocketWrapper.
                if hasattr(value, '_ensure_socket_exists'):
                    if value.is_input:
                        cls._input_descriptors[name] = value
                    else:
                        cls._output_descriptors[name] = value

        print_debug(f"--> Tag-Register class '{original_name}' (renamed to '{cls.__name__}') of type '{bpy_type.__name__}' --> Package: {cls.__module__}'")

        # Add to BTypes registry
        btype: BTypes = getattr(BTypes, bpy_type.__name__)
        btype.add_class(cls)

        return cls


# ----------------------------------------------------------------

def init():
    for subcls in BaseType.__subclasses_recursive__():
        if 'btypes' in subcls.__module__:
           # SKIP: IF THE SUBCLASS IS INSIDE THE some of the ackit module 'btypes' submodules where base types are at.
           print(f"INFO! SKIP: {subcls.__name__} - {subcls.__module__}")
           continue
        # print(f"INFO! tag register: {subcls.__name__} - {subcls.__module__}")
        subcls.tag_register()
