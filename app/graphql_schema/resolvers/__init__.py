from typing import Type, TypeVar

import strawberry
from fastapi import HTTPException, status
from graphql_schema.types import Context
from pydantic import BaseModel
from schemas import user as s_user

S = TypeVar(name="S", bound=BaseModel)
T = TypeVar(name="T")


def convert_to_type(input: S, type: Type[T]) -> T:
    """Converts a pydantic type to a stawberry type"""

    filtered_data = {
        k: v for k, v in input.model_dump().items() if k in type.__annotations__
    }

    return type(**filtered_data)


def get_context_user(info: strawberry.Info[Context]) -> s_user.User:
    current_user = info.context.user

    if not current_user:
        raise HTTPException(
            detail="User not authenticated",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return current_user
