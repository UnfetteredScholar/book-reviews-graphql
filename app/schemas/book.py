from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from schemas.base import PyObjectId


class Book(BaseModel):
    id: PyObjectId = Field(validation_alias="_id", default=None)
    isbn: str
    author_ids: List[str]
    title: str
    genres: List[str]
    series: Optional[str]
    series_number: Optional[float]
    pages: Optional[int]
    blurb: Optional[str]
    release_date: Optional[datetime]
    date_created: datetime
    date_modified: datetime


class BookIn(BaseModel):
    isbn: str
    author_ids: List[str]
    title: str
    series: Optional[str]
    series_number: Optional[float]
    pages: Optional[int]
    blurb: Optional[str]
    release_date: Optional[datetime]
