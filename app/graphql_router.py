from typing import List

import strawberry
from graph_dependencies.resolver import get_users
from graph_dependencies.schema import UserType
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Query:
    users: List[UserType] = strawberry.field(resolver=get_users)


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)
