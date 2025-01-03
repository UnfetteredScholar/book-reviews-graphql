from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator
from schemas.base import PyObjectId
from typing_extensions import Self


class Book(BaseModel):
    id: PyObjectId = Field(validation_alias="_id", default=None)
    isbn_10: Optional[str] = Field(min_length=10, max_length=10, default=None)
    isbn_13: Optional[str] = Field(min_length=13, max_length=13, default=None)
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

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.isbn_10 is None and self.isbn_13 is None:
            raise ValueError("At lease one isbn number must be set")
        return self


class BookIn(BaseModel):
    isbn_10: Optional[str] = Field(min_length=10, max_length=10, default=None)
    isbn_13: Optional[str] = Field(min_length=13, max_length=13, default=None)
    author_ids: List[str]
    title: str
    genres: List[str]
    series: Optional[str] = None
    series_number: Optional[float] = None
    pages: Optional[int] = None
    blurb: Optional[str] = None
    release_date: Optional[datetime] = None

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.isbn_10 is None and self.isbn_13 is None:
            raise ValueError("At lease one isbn number must be set")
        return self


class BookUpdate(BaseModel):
    isbn_10: Optional[str] = Field(min_length=10, max_length=10, default=None)
    isbn_13: Optional[str] = Field(min_length=13, max_length=13, default=None)
    author_ids: List[str] = []
    title: str = "None"
    genres: List[str] = []
    series: Optional[str] = None
    series_number: Optional[float] = None
    pages: Optional[int] = None
    blurb: Optional[str] = None
    release_date: Optional[datetime] = None
