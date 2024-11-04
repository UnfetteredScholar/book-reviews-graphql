from logging import getLogger
from typing import Type, TypeVar

import strawberry
from core.authentication.auth_middleware import authenticate_user
from core.authentication.auth_token import create_access_token
from core.storage import storage
from fastapi import HTTPException, status
from graphql_schema.types import Context, UserType
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


@strawberry.input
class UserInput:
    username: str = strawberry.field(description="The name of the user")
    email: str = strawberry.field(description="The user's email")
    password: str = strawberry.field(description="The user's password")


@strawberry.input
class LoginInput:
    email: str = strawberry.field(description="The user's email")
    password: str = strawberry.field(description="The user's password")


def get_user_me(info: strawberry.Info[Context]) -> UserType:
    """Gets a user"""
    current_user = info.context.user

    if not current_user:
        raise HTTPException(
            detail="User not authenticated", status_code=status.HTTP_401_UNAUTHORIZED
        )

    return convert_to_type(current_user, UserType)


def register_user(user_in: UserInput) -> UserType:
    """Registers a user"""
    logger = getLogger(__name__ + ".register_user")
    try:
        data = s_user.UserIn(
            username=user_in.username, email=user_in.email, password=user_in.password
        )
        id = storage.user_create_record(user_data=data)
        new_user = storage.user_verify_record({"_id": id})

        return convert_to_type(new_user, UserType)
    except Exception as ex:
        logger.error(ex)
        raise ex


def login_user(auth_input: LoginInput) -> str:
    """Authenticates a user and returns a jwt string"""
    logger = getLogger(__name__ + ".login_user")
    try:

        user = authenticate_user(email=auth_input.email, password=auth_input.password)

        logger.info("User Authenticated")

        if not user.verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account not verified",
            )

        token_data = {
            "sub": user.email,
            "id": user.id,
            "role": user.role,
            "type": "bearer",
        }
        access_token = create_access_token(token_data)
        logger.info(f"User ({user.id}) Token Generated")

        return access_token

    except Exception as ex:
        logger.error(ex)
        raise ex