from datetime import datetime
from functools import cached_property
from typing import Generic, List, Optional, TypeVar

import strawberry
from core.authentication.auth_middleware import get_current_user
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
    # reviews: List["ReviewType"]


@strawberry.type
class BookType:
    id: strawberry.ID
    isbn: str
    author_ids: List[str]
    title: str
    genres: List[str]
    series: Optional[str]
    series_number: Optional[float]
    pages: Optional[int]
    blurb: Optional[str]
    release_date: Optional[datetime]

    # Resolved
    authors: List["AuthorType"]
    # reviews: List["ReviewType"]


@strawberry.type
class AuthorType:
    id: strawberry.ID
    name: str
    bio: Optional[str]
    date_of_birth: Optional[datetime]
    gender: Optional[str]

    # Resolved
    # books: List[BookType]


@strawberry.type
class ReviewType:
    id: strawberry.ID
    user_id: str
    book_id: str
    rating: int
    title: Optional[str]
    content: Optional[str]
    # Resolved
    user: UserType
