from typing import List

import strawberry
from graphql_schema import resolvers as res
from graphql_schema.types import AuthorType, Page, UserType


@strawberry.type
class Query:
    # Users
    current_user: UserType = strawberry.field(
        resolver=res.get_user_me, description=res.get_user_me.__doc__
    )

    # Authors
    get_authors: Page[AuthorType] = strawberry.field(
        resolver=res.get_authors, description=res.get_authors.__doc__
    )
    get_author: AuthorType = strawberry.field(
        resolver=res.get_author, description=res.get_author.__doc__
    )
    # author: AuthorType
    # authors: List[AuthorType]


@strawberry.type
class Mutation:
    # Users
    register_user: UserType = strawberry.field(
        resolver=res.register_user, description=res.register_user.__doc__
    )
    login_user: str = strawberry.field(
        resolver=res.login_user, description=res.login_user.__doc__
    )

    # Authors
    add_author: AuthorType = strawberry.field(
        resolver=res.add_author, description=res.add_author.__doc__
    )

    update_author: AuthorType = strawberry.field(
        resolver=res.update_author, description=res.update_author.__doc__
    )

    delete_author: bool = strawberry.field(
        resolver=res.delete_author, description=res.delete_author.__doc__
    )
