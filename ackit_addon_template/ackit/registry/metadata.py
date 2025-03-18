from .reg_types import Node, NodeSocket, Operator



def Node(label: str | None = None, tooltip: str = "", icon: str = 'NONE') -> Node:
    def wrapper(cls):
        cls.bl_label = label or cls.__name__
        cls.bl_description = tooltip
        cls.bl_icon = icon
        return cls
    return wrapper


def NodeSocket(label: str | None = None, tooltip: str = "", subtype_label: str = '') -> Node:
    def wrapper(cls):
        cls.bl_label = label or cls.__name__
        cls.description = tooltip
        cls.bl_subtype_label = subtype_label
        return cls
    return wrapper

def Operator(label: str | None = None, tooltip: str = "") -> Node:
    def wrapper(cls):
        cls.bl_label = label or cls.__name__
        cls.bl_description = tooltip
        return cls
    return wrapper
