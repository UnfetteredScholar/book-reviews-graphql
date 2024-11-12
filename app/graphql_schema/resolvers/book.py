from dataclasses import asdict
from datetime import datetime
from logging import getLogger
from typing import List, Optional

import strawberry
from bson.objectid import ObjectId
from core.storage import storage
from fastapi import HTTPException, status
from graphql_schema import convert_to_type
from graphql_schema.resolvers import get_context_user
from graphql_schema.types import BookType, Context, Page, PageMeta
from schemas.book import Book, BookIn


@strawberry.input
class BookInput:
    isbn_10: Optional[str] = None
    isbn_13: Optional[str] = None
    author_ids: List[str]
    title: str
    genres: List[str]
    series: Optional[str] = None
    series_number: Optional[float] = None
    pages: Optional[int] = None
    blurb: Optional[str] = None
    release_date: Optional[datetime] = None


@strawberry.input
class BookUpdateInput:
    isbn_10: Optional[str] = strawberry.UNSET
    isbn_13: Optional[str] = strawberry.UNSET
    author_ids: List[str] = strawberry.UNSET
    title: str = strawberry.UNSET
    genres: List[str] = strawberry.UNSET
    series: Optional[str] = strawberry.UNSET
    series_number: Optional[float] = strawberry.UNSET
    pages: Optional[int] = strawberry.UNSET
    blurb: Optional[str] = strawberry.UNSET
    release_date: Optional[datetime] = strawberry.UNSET


def get_books(
    title: Optional[str] = None,
    limit: int = 10,
    cursor: Optional[str] = None,
) -> Page[BookType]:
    """Get books"""
    logger = getLogger(__name__ + ".get_book")
    try:
        filter = {}
        if title is not None:
            filter["title"] = title

        if cursor is not None:
            filter["_id"] = {"$gt": ObjectId(cursor)}

        books = storage.book_get_all_records(filter, limit=limit)

        next_cursor = None
        if books:
            next_cursor = books[-1].id
        books = [convert_to_type(book, BookType) for book in books]
        response: Page[BookType] = Page(
            items=books, page_meta=PageMeta(next_cursor=next_cursor)
        )

        return response

    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


def get_book(book_id: str) -> Book:
    """Gets an book by id"""
    logger = getLogger(__name__ + ".get_book")
    try:
        book = storage.book_verify_record({"_id": book_id})

        return convert_to_type(book, BookType)
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


def add_book(data: BookInput, info: strawberry.Info[Context]) -> BookType:
    """Creates an book record"""
    logger = getLogger(__name__ + ".add_book")
    try:
        get_context_user(info, role="admin")
        book_data = BookIn(**asdict(data))
        id = storage.book_create_record(book_data)

        book = storage.book_verify_record({"_id": id})

        return convert_to_type(book, BookType)
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


def update_book(
    data: BookUpdateInput, book_id: str, info: strawberry.Info[Context]
) -> Book:
    """Gets an book by id"""
    logger = getLogger(__name__ + ".update_book")
    try:
        get_context_user(info, role="admin")
        update = {}

        for k, v in asdict(data).items():
            if v is not strawberry.UNSET:
                update[k] = v

        storage.book_update_record(filter={"_id": book_id}, update=update)

        book = storage.book_verify_record({"_id": book_id})

        return convert_to_type(book, BookType)
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


def delete_book(book_id: str, info: strawberry.Info[Context]) -> bool:
    """deletes an book by id"""
    logger = getLogger(__name__ + ".delete_book")
    try:
        get_context_user(info, role="admin")
        storage.book_delete_record({"_id": book_id})

        return True

    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex
