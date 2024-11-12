from logging import getLogger
from typing import Optional

from core.authentication.auth_middleware import get_current_active_user
from core.authentication.role import allow_resource_admin
from core.storage import storage
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_pagination import Page
from schemas.author import Author, AuthorIn, AuthorUpdate
from schemas.user import User

router = APIRouter()


@router.get(path="/authors", response_model=Page[Author])
def get_authors(
    name: Optional[str] = None, current_user: User = Depends(get_current_active_user)
) -> Author:
    """Get  authors"""
    logger = getLogger(__name__ + ".get_author")
    try:
        filter = {}
        if name is not None:
            filter["name"] = name
        authors = storage.author_get_records_page(filter)

        return authors

    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


@router.get(path="/authors/{author_id}", response_model=Author)
def get_author(
    author_id: str, current_user: User = Depends(get_current_active_user)
) -> Author:
    """Gets an author by id"""
    logger = getLogger(__name__ + ".get_author")
    try:
        author = storage.author_verify_record({"_id": author_id})

        return author

    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


@router.post(
    path="/authors", response_model=Author, dependencies=[Depends(allow_resource_admin)]
)
def add_author(
    data: AuthorIn, current_user: User = Depends(get_current_active_user)
) -> Author:
    """Creates an author record"""
    logger = getLogger(__name__ + ".add_author")
    try:
        id = storage.author_create_record(data)

        return storage.author_verify_record({"_id": id})
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


@router.patch(
    path="/authors/{author_id}",
    response_model=Author,
    dependencies=[Depends(allow_resource_admin)],
)
def update_author(
    data: AuthorUpdate,
    author_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Author:
    """Gets an author by id"""
    logger = getLogger(__name__ + ".update_author")
    try:
        update = data.model_dump(exclude_unset=True)

        storage.author_update_record(filter={"_id": author_id}, update=update)

        return storage.author_verify_record({"_id": author_id})
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex


@router.delete(
    path="/authors/{author_id}",
    response_model=Author,
    dependencies=[Depends(allow_resource_admin)],
)
def delete_author(
    author_id: str, current_user: User = Depends(get_current_active_user)
) -> Author:
    """deletes an author by id"""
    logger = getLogger(__name__ + ".delete_author")
    try:
        storage.author_delete_record({"_id": author_id})

        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
        )

    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        raise ex
