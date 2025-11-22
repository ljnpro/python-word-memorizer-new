from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class WordBase(BaseModel):
    word: str
    phonetic: Optional[str] = None
    meaning: str
    example: Optional[str] = None
    tags: Optional[str] = None


class WordCreate(WordBase):
    pass


class WordUpdate(BaseModel):
    meaning: Optional[str] = None
    example: Optional[str] = None
    tags: Optional[str] = None
    phonetic: Optional[str] = None


class WordOut(WordBase):
    id: int
    familiarity_score: int
    created_at: datetime
    last_review_date: Optional[date]
    next_review_date: Optional[date]

    class Config:
        orm_mode = True
