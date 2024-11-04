import strawberry
from graphql_schema.resolvers import get_user_me, login_user, register_user
from graphql_schema.types import UserType


@strawberry.type
class Query:
    current_user: UserType = strawberry.field(resolver=get_user_me)


@strawberry.type
class Mutation:
    register_user: UserType = strawberry.field(resolver=register_user)
    login_user: str = strawberry.field(resolver=login_user)
