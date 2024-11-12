from typing import Type, TypeVar

from pydantic import BaseModel

S = TypeVar(name="S", bound=BaseModel)
T = TypeVar(name="T")


def convert_to_type(input: S, type: Type[T]) -> T:
    """Converts a pydantic type to a stawberry type"""

    filtered_data = {
        k: v for k, v in input.model_dump().items() if k in type.__annotations__
    }

    return type(**filtered_data)
