from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from schemas.base import PyObjectId


class Review(BaseModel):
    id: PyObjectId = Field(validation_alias="_id", default=None)
    user_id: str
    book_id: str
    rating: int
    title: Optional[str]
    content: Optional[str]
    date_created: datetime
    date_modified: datetime


class ReviewIn(BaseModel):
    # user_id: str
    # book_id: str
    rating: int
    title: Optional[str] = None
    content: Optional[str] = None
