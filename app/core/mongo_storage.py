from datetime import UTC, datetime
from typing import Dict, List, Optional

import gridfs
from bson.objectid import ObjectId
from core.authentication.hashing import hash_bcrypt
from core.config import settings
from fastapi import status
from fastapi.exceptions import HTTPException
from pymongo import ASCENDING
from pymongo.mongo_client import MongoClient
from schemas import user as s_user


class MongoStorage:
    """Storage class for interfacing with mongo db"""

    def __init__(self, db_name: str = settings.DATABSE_NAME):
        """Initializes a MongoStorage object"""

        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[db_name]
        self.fs = gridfs.GridFS(self.db)

        # Create indexes
        self.db["users"].create_index(keys=[("email", ASCENDING)], unique=True)

    # users
    def user_create_record(
        self,
        user_data: s_user.UserIn,
        role: s_user.Role = "user",
        sign_in_type: s_user.SignInType = "NORMAL",
        verified: bool = False,
    ) -> str:
        """Creates a user record"""

        users_table = self.db["users"]

        if users_table.find_one({"email": user_data.email}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken",
            )

        if len(user_data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password length."
                + " Password length must be at least 8 characters",
            )

        date = datetime.now(UTC)
        user = user_data.model_dump()
        user["password"] = hash_bcrypt(user_data.password)
        user["role"] = role
        user["sign_in_type"] = sign_in_type
        user["verified"] = verified
        user["status"] = s_user.UserStatus.ENABLED
        user["date_created"] = date
        user["date_modified"] = date

        id = str(users_table.insert_one(user).inserted_id)

        return id

    def user_get_record(self, filter: Dict) -> Optional[s_user.User]:
        """Gets a user record from the db using the supplied filter"""
        users = self.db["users"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        user = users.find_one(filter)

        if user:
            user = s_user.User(**user)

        return user

    def user_get_all_records(self, filter: Dict) -> List[s_user.User]:
        """Gets all user records from the db using the supplied filter"""
        users = self.db["users"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        users_list = users.find(filter)

        users_list = [s_user.User(**user) for user in users_list]

        return users_list

    def user_verify_record(self, filter: Dict) -> s_user.User:
        """
        Gets a user record using the filter
        and raises an error if a matching record is not found
        """

        user = self.user_get_record(filter)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    def user_update_record(self, filter: Dict, update: Dict):
        """Updates a user record"""
        self.user_verify_record(filter)

        for key in ["_id", "email"]:
            if key in update:
                raise KeyError(f"Invalid Key. KEY {key} cannot be changed")
        update["date_modified"] = datetime.now(UTC)

        return self.db["users"].update_one(filter, {"$set": update})

    def user_delete_record(self, filter: Dict):
        """Deletes a user record"""
        self.user_verify_record(filter)

        self.db["users"].delete_one(filter)
