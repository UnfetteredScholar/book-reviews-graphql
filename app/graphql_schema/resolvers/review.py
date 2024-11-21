from dataclasses import asdict
from logging import getLogger
from typing import Optional

import strawberry
from bson.objectid import ObjectId
from core.storage import storage
from fastapi import HTTPException, status
from graphql_schema import convert_to_type
from graphql_schema.resolvers import get_context_user
from graphql_schema.types import Context, Page, PageMeta, ReviewType
from schemas import review as p


@strawberry.input
class ReviewInput:
    rating: int
    title: Optional[str] = None
    content: Optional[str] = None


@strawberry.input
class ReviewUpdateInput:
    rating: int = strawberry.UNSET
    title: Optional[str] = strawberry.UNSET
    content: Optional[str] = strawberry.UNSET


def get_reviews(
    book_id: str,
    limit: int = 10,
    cursor: Optional[str] = None,
) -> Page[ReviewType]:
    """Gets the reviews of a book"""
    logger = getLogger(__name__ + ".get_reviews")
    try:
        storage.book_verify_record({"_id": book_id})
        filter = {"book_id": book_id}
        if cursor is not None:
            filter["_id"] = {"$gt": {ObjectId(cursor)}}

        reviews = storage.review_get_all_records(filter=filter, limit=limit)

        next_cursor = None
        if reviews:
            next_cursor = reviews[-1].id

        reviews = [convert_to_type(review, ReviewType) for review in reviews]
        response: Page[ReviewType] = Page(
            items=reviews, page_meta=PageMeta(next_cursor=next_cursor)
        )

        return response
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
            )
        raise ex


def get_review(review_id: str) -> ReviewType:
    """Gets a review by its id"""
    logger = getLogger(__name__ + ".get_review")
    try:

        review = storage.review_verify_record({"_id": review_id})

        return convert_to_type(review, ReviewType)
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
            )
        raise ex


def add_review(
    book_id: str, review_data: ReviewInput, info: strawberry.Info[Context]
) -> ReviewType:
    """Adds a review to a book"""
    logger = getLogger(__name__ + ".add_review")
    try:
        current_user = get_context_user(info)
        storage.book_verify_record({"_id": book_id})

        id = storage.review_create_record(
            review_data=p.ReviewIn(**asdict(review_data)),
            user_id=current_user.id,
            book_id=book_id,
        )
        review = storage.review_verify_record({"_id": id})

        return convert_to_type(review, ReviewType)
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
            )
        raise ex


def update_review(
    review_id: str, review_data: ReviewUpdateInput, info: strawberry.Info[Context]
) -> ReviewType:
    """Updates a book review"""
    logger = getLogger(__name__ + ".update_review")
    try:
        current_user = get_context_user(info)
        update = {}

        for k, v in asdict(review_data).items():
            if v is not strawberry.UNSET:
                update[k] = v

        storage.review_update_record(
            filter={"_id": review_id, "user_id": current_user.id}, update=update
        )

        review = storage.review_verify_record({"_id": review_id})

        return convert_to_type(**asdict(review))
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
            )
        raise ex


def delete_review(review_id: str, info: strawberry.Info[Context]) -> bool:
    """Deletes a review by its id"""
    logger = getLogger(__name__ + ".delete_review")
    try:
        current_user = get_context_user(info)
        storage.review_delete_record({"_id": review_id, "user_id": current_user.id})

        return True
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
            )
        raise ex
