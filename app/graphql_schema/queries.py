import strawberry
from graphql_schema.resolvers import author, user
from graphql_schema.types import AuthorType, Page, UserType


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
    # author: AuthorType
    # authors: List[AuthorType]


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
