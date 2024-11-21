import strawberry
from graphql_schema.resolvers import author, book, review, user
from graphql_schema.types import AuthorType, BookType, Page, ReviewType, UserType


@strawberry.type
class Query:
    # Users
    current_user: UserType = strawberry.field(
        resolver=user.get_user_me, description=user.get_user_me.__doc__
    )

    # Authors
    get_authors: Page[AuthorType] = strawberry.field(
        resolver=author.get_authors, description=author.get_authors.__doc__
    )
    get_author: AuthorType = strawberry.field(
        resolver=author.get_author, description=author.get_author.__doc__
    )

    # Books
    get_books: Page[BookType] = strawberry.field(
        resolver=book.get_books, description=book.get_books.__doc__
    )
    get_book: BookType = strawberry.field(
        resolver=book.get_book, description=book.get_book.__doc__
    )

    # Reviews
    get_reviews: Page[ReviewType] = strawberry.field(
        resolver=review.get_reviews, description=review.get_reviews.__doc__
    )
    get_review: ReviewType = strawberry.field(
        resolver=review.get_review, description=review.get_review.__doc__
    )


@strawberry.type
class Mutation:
    # Users
    register_user: UserType = strawberry.field(
        resolver=user.register_user, description=user.register_user.__doc__
    )
    login_user: str = strawberry.field(
        resolver=user.login_user, description=user.login_user.__doc__
    )

    # Authors
    add_author: AuthorType = strawberry.field(
        resolver=author.add_author, description=author.add_author.__doc__
    )

    update_author: AuthorType = strawberry.field(
        resolver=author.update_author, description=author.update_author.__doc__
    )

    delete_author: bool = strawberry.field(
        resolver=author.delete_author, description=author.delete_author.__doc__
    )

    # Books
    add_book: BookType = strawberry.field(
        resolver=book.add_book, description=book.add_book.__doc__
    )

    update_book: BookType = strawberry.field(
        resolver=book.update_book, description=book.update_book.__doc__
    )

    delete_book: bool = strawberry.field(
        resolver=book.delete_book, description=book.delete_book.__doc__
    )

    # Reviews
    add_review: ReviewType = strawberry.field(
        resolver=review.add_review, description=review.add_review.__doc__
    )

    update_review: ReviewType = strawberry.field(
        resolver=review.update_review, description=review.update_review.__doc__
    )

    delete_review: bool = strawberry.field(
        resolver=review.delete_review, description=review.delete_review.__doc__
    )
