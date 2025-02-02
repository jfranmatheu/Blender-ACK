from ..register import BTypes

from ..types.ops import OperatorTypes
from .ops_options import OperatorOptionsDecorators
from .polling import Polling


__all__ = ['OperatorDecorators']


class OperatorDecorators:
    GENERIC = OperatorTypes.GENERIC
    ACTION = OperatorTypes.ACTION
    MODAL = OperatorTypes.MODAL
