from typing import TypeVar, Generic, Any, Type, cast, get_origin, Callable, Optional


T = TypeVar('T')

class SocketCast(Generic[T]):
    def __init__(self, cast_func: Callable[[Any], T], poll_func: Optional[Callable[[Any], bool]] = None) -> None:
        self.cast_func = cast_func
        self.poll_func = poll_func
        
    def poll_value(self, value: Any) -> bool:
        if self.poll_func is None:
            return True
        return self.poll_func(value)

    def cast(self, value: Any) -> T:
        if not self.poll_value(value):
            raise ValueError(f"Value {value} cannot be cast to {self.get_cast_type()}. Reason: poll function failed.")
        return self.cast_func(value)

    def get_cast_type(self) -> Type[T]:
        # self.cast_func.__annotations__['return']
        return get_origin(self.__class__.__orig_bases__[0])
