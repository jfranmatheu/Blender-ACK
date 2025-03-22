from .ops import generate_ops_py
from .icons import generate_icons_py
from .types import generate_types_py

__all__ = ['AutoCode']


class AutoCode:
    @staticmethod
    def OPS(filename: str = 'ops'):
        ''' Generate a {filename}.py file with typed operator classes. '''
        generate_ops_py(filename)

    @staticmethod
    def ICONS(filename: str = 'icons'):
        ''' Generate a {filename}.py file with an Icon class to get icons to draw in Blender interface or custom interfaces. '''
        generate_icons_py(filename)
        
    @staticmethod
    def TYPES(filename: str = 'types'):
        ''' Generate a {filename}.py file with typed PropertyGroup classes, as well as AddonPreferences and extended bpy.types. '''
        generate_types_py(filename)
