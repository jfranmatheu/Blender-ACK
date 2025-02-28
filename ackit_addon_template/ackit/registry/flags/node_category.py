from typing import Type

from ..reg_types.nodes import T


def node_category(category: str):
    """
    Decorator to add a node category to a node class.
    
    Args:
        category (str): The specific node category to add. Use '/' to specify subcategories.
    
    Returns:
        Callable: A decorator function that modifies the node class to include the specified category to the node.
    """
    def wrapper(cls: Type[T]) -> Type[T]:
        cls._node_category = category
        return cls
    return wrapper
