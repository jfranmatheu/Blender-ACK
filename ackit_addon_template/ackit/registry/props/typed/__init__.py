from .descriptors import *
from .wrapped import WrappedTypedPropertyTypes


__all__ = ['DescriptorTypedPropertyTypes', 'WrappedTypedPropertyTypes']


class DescriptorTypedPropertyTypes:
    BOOL = BoolProperty
    FLOAT = FloatProperty
    VECTOR_FLOAT = FloatVectorProperty
    INT = IntProperty
    VECTOR_INT = IntVectorProperty
    STRING = StringProperty
    ENUM = EnumProperty
    POINTER = PointerProperty
    COLLECTION = CollectionProperty
