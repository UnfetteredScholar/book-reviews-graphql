from datetime import UTC, datetime
from typing import Dict, List, Optional

import gridfs
from bson.objectid import ObjectId
from core.authentication.hashing import hash_bcrypt
from core.config import settings
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.pymongo import paginate
from pymongo import ASCENDING
from pymongo.mongo_client import MongoClient
from schemas import author as s_author
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

    # authors
    def author_create_record(
        self,
        author_data: s_author.AuthorIn,
    ) -> str:
        """Creates an author record"""

        authors_table = self.db["authors"]

        date = datetime.now(UTC)
        author = s_author.Author(
            name=author_data.name,
            bio=author_data.bio,
            date_of_birth=author_data.date_of_birth,
            gender=author_data.gender,
            date_created=date,
            date_modified=date,
        )

        id = str(
            authors_table.insert_one(author.model_dump(exclude_unset=True)).inserted_id
        )

        return id

    def author_get_record(self, filter: Dict) -> Optional[s_author.Author]:
        """Gets a author record from the db using the supplied filter"""
        authors = self.db["authors"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        author = authors.find_one(filter)

        if author:
            author = s_author.Author(**author)

        return author

    def author_get_all_records(
        self, filter: Dict, limit: Optional[int] = None
    ) -> List[s_author.Author]:
        """Gets all author records from the db using the supplied filter"""
        authors = self.db["authors"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        authors_list = authors.find(filter).sort({"_id": ASCENDING})

        if limit is not None:
            authors_list = authors_list.limit(limit)

        authors_list = [s_author.Author(**author) for author in authors_list]

        return authors_list

    def author_get_records_page(self, filter: Dict) -> Page[s_author.Author]:
        """Gets a page of author records from the db using the supplied filter"""
        authors = self.db["authors"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        result = paginate(collection=authors, query_filter=filter)

        return result

    def author_verify_record(self, filter: Dict) -> s_author.Author:
        """
        Gets a author record using the filter
        and raises an error if a matching record is not found
        """

        author = self.author_get_record(filter)

        if author is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
            )

        return author

    def author_update_record(self, filter: Dict, update: Dict):
        """Updates a author record"""
        self.author_verify_record(filter)

        for key in ["_id"]:
            if key in update:
                raise KeyError(f"Invalid Key. KEY {key} cannot be changed")
        update["date_modified"] = datetime.now(UTC)

        return self.db["authors"].update_one(filter, {"$set": update})

    def author_delete_record(self, filter: Dict):
        """Deletes a author record"""
        self.author_verify_record(filter)

        self.db["authors"].delete_one(filter)
