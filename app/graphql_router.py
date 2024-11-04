import strawberry
from graphql_schema.queries import Mutation, Query
from graphql_schema.types import Context
from strawberry.fastapi import GraphQLRouter


async def get_context() -> Context:
    return Context()


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema, context_getter=get_context)
