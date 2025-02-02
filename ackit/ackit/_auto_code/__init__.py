from enum import Enum

from .ops import generate_ops_py


__all__ = ['AutoCode']


class AutoCode(Enum):
    OPS = generate_ops_py

    @property
    def func(self):
        return self.value

    def __call__(self):
        self.func()
