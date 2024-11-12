from logging import getLogger
from typing import Optional

from core.authentication.auth_middleware import get_current_active_user
from core.authentication.role import allow_resource_admin
from core.storage import storage
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_pagination import Page
from schemas.book import Book, BookIn, BookUpdate
from schemas.user import User

router = APIRouter()


@router.get(path="/books", response_model=Page[Book])
def get_books(title: Optional[str] = None) -> Book:
    """Get books"""
    logger = getLogger(__name__ + ".get_book")
    try:
        filter = {}
        if title is not None:
            filter["title"] = title
        books = storage.book_get_records_page(filter)

        return books

    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


@router.get(path="/books/{book_id}", response_model=Book)
def get_book(book_id: str) -> Book:
    """Gets an book by id"""
    logger = getLogger(__name__ + ".get_book")
    try:
        book = storage.book_verify_record({"_id": book_id})

        return book
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


@router.post(
    path="/books", response_model=Book, dependencies=[Depends(allow_resource_admin)]
)
def add_book(
    data: BookIn, current_user: User = Depends(get_current_active_user)
) -> Book:
    """Creates an book record"""
    logger = getLogger(__name__ + ".add_book")
    try:
        id = storage.book_create_record(data)

        return storage.book_verify_record({"_id": id})
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


@router.patch(
    path="/books/{book_id}",
    response_model=Book,
    dependencies=[Depends(allow_resource_admin)],
)
def update_book(
    data: BookUpdate,
    book_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Book:
    """Gets an book by id"""
    logger = getLogger(__name__ + ".update_book")
    try:
        update = data.model_dump(exclude_unset=True)

        storage.book_update_record(filter={"_id": book_id}, update=update)

        return storage.book_verify_record({"_id": book_id})
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


@router.delete(
    path="/books/{book_id}",
    response_model=Book,
    dependencies=[Depends(allow_resource_admin)],
)
def delete_book(
    book_id: str, current_user: User = Depends(get_current_active_user)
) -> Book:
    """deletes an book by id"""
    logger = getLogger(__name__ + ".delete_book")
    try:
        storage.book_delete_record({"_id": book_id})

        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
        )

    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex
