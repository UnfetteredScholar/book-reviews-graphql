from dataclasses import asdict
from datetime import date
from logging import getLogger
from typing import Optional

import strawberry
from bson.objectid import ObjectId
from core.storage import storage
from fastapi import HTTPException, status
from graphql_schema.resolvers import convert_to_type, get_context_user
from graphql_schema.types import AuthorType, Context, Page, PageMeta
from schemas import author as s_author


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
