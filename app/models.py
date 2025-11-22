from datetime import datetime, date, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Date

from .database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True, index=True, nullable=False)
    phonetic = Column(String, nullable=True)
    meaning = Column(String, nullable=False)
    example = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    familiarity_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_review_date = Column(Date, nullable=True)
    next_review_date = Column(Date, nullable=True, index=True)

    def is_new(self) -> bool:
        return self.familiarity_score == 0

    def mark_known(self):
        self.familiarity_score = min(5, (self.familiarity_score or 0) + 1)
        self.last_review_date = date.today()
        self.next_review_date = self.calculate_next_review_date()

    def mark_unknown(self):
        self.familiarity_score = max(0, (self.familiarity_score or 0) - 1)
        self.last_review_date = date.today()
        self.next_review_date = date.today() + timedelta(days=1)

    def calculate_next_review_date(self) -> date:
        intervals = {
            0: 1,
            1: 2,
            2: 4,
            3: 7,
            4: 14,
            5: 30,
        }
        days = intervals.get(self.familiarity_score, 1)
        return date.fromordinal(date.today().toordinal() + days)
