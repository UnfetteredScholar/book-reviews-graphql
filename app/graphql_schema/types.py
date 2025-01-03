from datetime import datetime
from functools import cached_property
from typing import Generic, List, Optional, TypeVar

import strawberry
from bson.objectid import ObjectId
from core.authentication.auth_middleware import get_current_user
from core.storage import storage
from graphql_schema import convert_to_type
from schemas.user import Role, SignInType, User, UserStatus
from strawberry.fastapi import BaseContext


class Context(BaseContext):
    @cached_property
    def user(self) -> User | None:
        if not self.request:
            return None

        authorization = self.request.headers.get("Authorization", None)
        if authorization:
            token = authorization.split(" ")[-1]
            return get_current_user(token=token)


@strawberry.type
class PageMeta:
    next_cursor: Optional[str] = strawberry.field(
        description="The next cursor to continue with."
    )


T = TypeVar("T")


@strawberry.type
class Page(Generic[T]):
    items: List[T]
    page_meta: PageMeta


@strawberry.type
class UserType:
    id: strawberry.ID
    username: str
    email: str
    # password: str
    role: Role
    status: UserStatus
    sign_in_type: SignInType
    verified: bool
    date_created: datetime
    date_modified: datetime

    # Resolved
    @strawberry.field
    def reviews(self) -> List["ReviewType"]:
        """Gets a user's reviews"""

        reviews = storage.review_get_all_records({"user_id": self.id})
        reviews = [convert_to_type(review, ReviewType) for review in reviews]

        return reviews


@strawberry.type
class BookType:
    id: strawberry.ID
    isbn_10: Optional[str]
    isbn_13: Optional[str]
    author_ids: List[str]
    title: str
    genres: List[str]
    series: Optional[str]
    series_number: Optional[float]
    pages: Optional[int]
    blurb: Optional[str]
    release_date: Optional[datetime]

    # Resolved
    @strawberry.field
    def authors(self) -> List["AuthorType"]:
        """The book's authors"""
        ids = [ObjectId(id) for id in self.author_ids]

        authors = storage.author_get_all_records({"_id": {"$in": ids}})
        authors = [convert_to_type(author, AuthorType) for author in authors]

        return authors

    @strawberry.field
    def reviews(self) -> List["ReviewType"]:
        """Gets a book's reviews"""

        reviews = storage.review_get_all_records({"book_id": self.id})
        reviews = [convert_to_type(review, ReviewType) for review in reviews]

        return reviews


@strawberry.type
class AuthorType:
    id: strawberry.ID
    name: str
    bio: Optional[str]
    date_of_birth: Optional[datetime]
    gender: Optional[str]

    # Resolved
    @strawberry.field(description="Gets the author's books")
    def books(self) -> List[BookType]:
        """Gets the author's books"""
        filter = {"author_ids": self.id}
        books = storage.book_get_all_records(filter=filter)

        books = [convert_to_type(book, BookType) for book in books]

        return books


@strawberry.type
class ReviewType:
    id: strawberry.ID
    user_id: str
    book_id: str
    rating: int
    title: Optional[str]
    content: Optional[str]

    # Resolved
    @strawberry.field
    def user(self) -> UserType:
        """Gets the user of a review"""
        user = storage.user_verify_record({"_id": self.user_id})
        return convert_to_type(user, UserType)
