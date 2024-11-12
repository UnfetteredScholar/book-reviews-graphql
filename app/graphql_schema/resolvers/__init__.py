import strawberry
from fastapi import HTTPException, status
from graphql_schema.types import Context
from schemas import user as s_user


def get_context_user(
    info: strawberry.Info[Context], role: s_user.Role = s_user.Role.USER
) -> s_user.User:
    current_user = info.context.user

    if not current_user:
        raise HTTPException(
            detail="User not authenticated",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if role == s_user.Role.ADMIN:
        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User role not permitted to perform this action",
            )

    return current_user
