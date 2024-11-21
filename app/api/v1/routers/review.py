from logging import getLogger

from core.authentication.auth_middleware import get_current_active_user
from core.storage import storage
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_pagination import Page
from schemas import review as p
from schemas.user import User

router = APIRouter()


@router.get(path="/books/{book_id}/reviews", response_model=Page[p.Review])
def get_reviews(book_id: str) -> Page[p.Review]:
    """Gets the reviews of a book"""
    logger = getLogger(__name__ + ".get_reviews")
    try:
        storage.book_verify_record({"_id": book_id})

        reviews = storage.review_get_records_page({"book_id": book_id})

        return reviews
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
            )
        raise ex


@router.get(path="/reviews/{review_id}", response_model=p.Review)
def get_review(review_id: str) -> p.Review:
    """Gets a review by its id"""
    logger = getLogger(__name__ + ".get_review")
    try:

        review = storage.review_verify_record({"_id": review_id})

        return review
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
            )
        raise ex


@router.post(path="/books/{book_id}/reviews", response_model=p.Review)
def add_review(
    book_id: str,
    review_data: p.ReviewIn,
    current_user: User = Depends(get_current_active_user),
) -> p.Review:
    """Adds a review to a book"""
    logger = getLogger(__name__ + ".add_review")
    try:
        storage.book_verify_record({"_id": book_id})

        id = storage.review_create_record(
            review_data=review_data, user_id=current_user.id, book_id=book_id
        )

        return storage.review_verify_record({"_id": id})
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
            )
        raise ex


@router.patch(path="/reviews/{review_id}", response_model=p.Review)
def update_review(
    review_id: str,
    review_data: p.ReviewUpdate,
    current_user: User = Depends(get_current_active_user),
) -> p.Review:
    """Adds a review to a book"""
    logger = getLogger(__name__ + ".update_review")
    try:
        update = review_data.model_dump(exclude_unset=True)

        storage.review_update_record(
            filter={"_id": review_id, "user_id": current_user.id}, update=update
        )

        return storage.review_verify_record({"_id": review_id})
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
            )
        raise ex


@router.delete(path="/reviews/{review_id}")
def delete_review(
    review_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """Deletes a review by its id"""
    logger = getLogger(__name__ + ".delete_review")
    try:

        storage.review_delete_record({"_id": review_id, "user_id": current_user.id})

        return JSONResponse(
            content={"message": "Review deleted"}, status_code=status.HTTP_202_ACCEPTED
        )
    except Exception as ex:
        logger.error(ex)
        if type(ex) is not HTTPException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
            )
        raise ex
