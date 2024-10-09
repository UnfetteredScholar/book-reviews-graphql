from datetime import datetime

import strawberry
from schemas.user import Role, SignInType, UserStatus


@strawberry.type
class UserType:
    id: str
    username: str
    email: str
    password: str
    role: Role
    status: UserStatus
    sign_in_type: SignInType
    verified: bool
    date_created: datetime
    date_modified: datetime
