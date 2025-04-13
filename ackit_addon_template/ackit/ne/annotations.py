from typing import Type, TypeVar

# Assuming these are the internal implementation classes
from .annotations_internal import NodeSocketInput as _NodeSocketInput, NodeSocketOutput as _NodeSocketOutput
# Import the base NodeSocket type if needed for type hinting
from .btypes.node_socket import NodeSocket
# Import specific socket types if needed, though the TypeVar approach might suffice
from . import socket_types # Assuming socket_types defines the actual NodeSocketFloat etc.


# Definir TypeVar. Esto nos ayuda a tener tipado del tipo de NodeSocket suyacente,
# el cual usamos para definir el tipo de socket para inputs y outputs.
SocketT = TypeVar('SocketT', bound=NodeSocket)


# Explicitly annotate the NodeInput and NodeOutput with proper signatures
def NodeInput(socket_type: Type[SocketT], multi: bool = False) -> SocketT:
    """
    Create an input socket annotation.
    
    Args:
        socket_type: The type of node socket (e.g., socket_types.NodeSocketFloat)
        multi: Whether this is a multi-input socket
        
    Returns:
        The actual socket instance (typed as SocketT) when accessed on a node instance.
    """
    # Call the correctly typed internal function
    # The type ignore might still be needed if the IDE struggles with the descriptor protocol
    return _NodeSocketInput(socket_type, multi) # type: ignore

def NodeOutput(socket_type: Type[SocketT]) -> SocketT:
    """
    Create an output socket annotation.
    
    Args:
        socket_type: The type of node socket (e.g., socket_types.NodeSocketFloat)
        
    Returns:
        The actual socket instance (typed as SocketT) when accessed on a node instance.
    """
    # Call the correctly typed internal function
    # The type ignore might still be needed
    return _NodeSocketOutput(socket_type) # type: ignore 
