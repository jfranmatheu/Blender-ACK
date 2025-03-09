from typing import Dict, Set, Type, List, Tuple
from collections import defaultdict

from ..props.typed.wrapped import WrappedPropertyDescriptor


__all__ = ['register_property', 'batch_register_properties']


to_register_properties: Dict[Type, Dict[str, WrappedPropertyDescriptor]] = defaultdict(dict)
to_unregister_properties: List[Tuple[Type, str]] = []


def register_property(bpy_type, property_idname: str, property: WrappedPropertyDescriptor, remove_on_unregister: bool = False):
    ''' DON'T USE AS DECORATOR. USE IT AS A TYPICAL FUNCTION.
        USE IT INSIDE A 'def register()' anywhere in your addon's source.

        Parameters:
            - 'bpy_type': some Blender ID type from 'bpy.types' submodule. It can be an string too. (examples: bpy.types.Scene or... 'Scene' or... 'SCENE')
            - 'property_idname': identifier of the property.
            - 'property': property definition (use ACK.PropsWrapped).
            - 'remove_on_unregister': whether to remove property on unregister or not.
    '''
    if not isinstance(property, WrappedPropertyDescriptor):
        raise ValueError(f"Provided property is not a valid WrappedPropertyDescriptor. {type(property)}")
    if bpy_type.__module__ != 'bpy_types':
        raise ValueError(f"Provided bpy_type is not a valid Blender type. {type(bpy_type)}")

    to_register_properties[bpy_type][property_idname] = property

    if remove_on_unregister:
        to_unregister_properties.append((bpy_type, property_idname))


def batch_register_properties(bpy_type: Type, *properties: Tuple[str, WrappedPropertyDescriptor], *, remove_on_unregister: bool = False):
    for property_idname, property_wrapper in properties:
        register_property(bpy_type, property_idname, property_wrapper, remove_on_unregister=remove_on_unregister)


# -------------------------------------------------------------------------------------------------


def register():
    for bpy_type, properties in to_register_properties.items():
        for property_idname, property_wrapper in properties.items():
            property_wrapper.create_property(property_idname, bpy_type)

def unregister():
    for bpy_type, prop_idname in to_unregister_properties:
        if hasattr(bpy_type, prop_idname):
            delattr(bpy_type, prop_idname)
