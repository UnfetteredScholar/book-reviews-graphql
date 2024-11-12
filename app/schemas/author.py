from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from schemas.base import PyObjectId


class Author(BaseModel):
    id: PyObjectId = Field(validation_alias="_id", default=None)
    name: str
    bio: Optional[str]
    date_of_birth: Optional[datetime]
    gender: Optional[str]
    date_created: datetime
    date_modified: datetime


class AuthorIn(BaseModel):
    name: str
    bio: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None


class AuthorUpdate(BaseModel):
    name: str = "None"
    bio: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
