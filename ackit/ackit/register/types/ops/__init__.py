from typing import TypeVar

import bpy

from .ot_generic import Generic as Operator_Generic
from .ot_action import Action as Operator_Action
from .ot_modal import Modal as Operator_Modal


__all__ = [
    'OperatorTypes',
    'T',
]


# Create a virtual type that combines bpy and ackit Operator types for proper typing.
T = TypeVar('T', bound=bpy.types.Operator | Operator_Generic)


class OperatorTypes:
    GENERIC = Operator_Generic
    ACTION = Operator_Action
    MODAL = Operator_Modal
