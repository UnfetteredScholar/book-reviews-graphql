from typing import List

from core.storage import storage
from graph_dependencies.schema import UserType


def get_users() -> List[UserType]:
    """Gets users"""
    users = storage.user_get_all_records({})

    users_list = [UserType(**user.model_dump()) for user in users]

    return users_list
