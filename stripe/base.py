from __future__ import annotations
from abc import abstractmethod
from types import TracebackType
from typing import Optional, Union, Sequence, Type
from stripe.config import StripeConfig
from type import NeoColor


class Base:
    @abstractmethod
    def __init__(self, config: StripeConfig):
        pass

    @abstractmethod
    def deinit(self):
        pass


    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        self.deinit()

    @abstractmethod
    def fill(self, color: NeoColor, send: bool = True):
        pass

    @abstractmethod
    def set_pixel(self, index: Union[int, slice], color: Union[NeoColor, Sequence[NeoColor]], send: bool = True):
        pass

    @abstractmethod
    def get_pixels(self, *indexes):
        pass

    @property
    @abstractmethod
    def brightness(self):
        pass

    @brightness.setter
    @abstractmethod
    def brightness(self, value: float):
        pass

    @property
    @abstractmethod
    def chain_count(self):
        pass
