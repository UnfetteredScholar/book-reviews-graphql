from dataclasses import asdict
from datetime import date
from logging import getLogger
from typing import List, Optional, Type, TypeVar

import strawberry
from bson.objectid import ObjectId
from core.authentication.auth_middleware import authenticate_user
from core.authentication.auth_token import create_access_token
from core.storage import storage
from fastapi import HTTPException, status
from graphql_schema.types import AuthorType, Context, Page, PageMeta, UserType
from pydantic import BaseModel
from schemas import author as s_author
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


# Users


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
    logger = getLogger(__name__ + ".get_user_me")
    try:
        current_user = get_context_user(info)

        return convert_to_type(current_user, UserType)
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


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
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
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
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


# Authors


@strawberry.input
class AuthorInput:
    name: str
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None


@strawberry.input
class AuthorUpdateInput:
    name: str = strawberry.UNSET
    bio: Optional[str] = strawberry.UNSET
    date_of_birth: Optional[date] = strawberry.UNSET
    gender: Optional[str] = strawberry.UNSET


def get_author(author_id: str) -> AuthorType:
    """Gets an author by id"""
    logger = getLogger(__name__ + ".get_author")
    try:
        author = storage.author_verify_record({"_id": author_id})

        return convert_to_type(author, AuthorType)
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


def get_authors(
    limit: int = 10,
    name: Optional[str] = None,
    cursor: Optional[str] = None,
) -> Page[AuthorType]:
    """
    Gets available authors
    When name is set gets authors matching the name
    """
    logger = getLogger(__name__ + ".get_authors")
    try:
        filter = {}
        if name is not None:
            filter["name"] = name

        if cursor is not None:
            filter["_id"] = {"$gt": ObjectId(cursor)}
        authors = storage.author_get_all_records(filter=filter, limit=limit)

        next_cursor = None
        if authors:
            next_cursor = authors[-1].id
        authors = [convert_to_type(author, AuthorType) for author in authors]
        response: Page[AuthorType] = Page(
            items=authors, page_meta=PageMeta(next_cursor=next_cursor)
        )

        return response
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


def add_author(data: AuthorInput, info: strawberry.Info[Context]) -> AuthorType:
    """Creates an author record"""
    logger = getLogger(__name__ + ".add_author")
    try:
        get_context_user(info)
        author_input = s_author.AuthorIn(**asdict(data))
        id = storage.author_create_record(author_data=author_input)

        return storage.author_verify_record({"_id": id})
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


def update_author(
    data: AuthorUpdateInput,
    author_id: str,
) -> AuthorType:
    """Updates an author by id"""
    logger = getLogger(__name__ + ".update_author")
    try:

        update = {}

        for k, v in asdict(data).items():
            if v is not strawberry.UNSET:
                update[k] = v

        storage.author_update_record(filter={"_id": author_id}, update=update)

        return storage.author_verify_record({"_id": author_id})
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


def delete_author(author_id: str, info: strawberry.Info[Context]) -> bool:
    """deletes an author by id"""
    logger = getLogger(__name__ + ".delete_author")
    try:
        get_context_user(info)
        storage.author_delete_record({"_id": author_id})

        return True
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex
