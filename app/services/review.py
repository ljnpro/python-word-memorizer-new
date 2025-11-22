from datetime import date
from typing import List, Tuple

from sqlalchemy.orm import Session

from app import models

NEW_WORD_LIMIT = 20
MAX_REVIEW_TASKS = 100


def get_today_review_words(db: Session) -> List[models.Word]:
    today = date.today()

    due_words = (
        db.query(models.Word)
        .filter(models.Word.next_review_date != None)  # noqa: E711
        .filter(models.Word.next_review_date <= today)
        .order_by(models.Word.familiarity_score.asc(), models.Word.next_review_date.asc())
        .all()
    )

    # supplement with new words if under limit
    if len(due_words) < MAX_REVIEW_TASKS:
        needed = min(NEW_WORD_LIMIT, MAX_REVIEW_TASKS - len(due_words))
        new_words = (
            db.query(models.Word)
            .filter((models.Word.next_review_date == None) | (models.Word.familiarity_score == 0))  # noqa: E711
            .order_by(models.Word.created_at.asc())
            .limit(needed)
            .all()
        )
        for w in new_words:
            if w.next_review_date is None:
                w.next_review_date = today
        db.commit()
        due_words.extend([w for w in new_words if w not in due_words])

    # cap total
    return due_words[:MAX_REVIEW_TASKS]


def apply_review_action(word: models.Word, known: bool) -> None:
    if known:
        word.mark_known()
    else:
        word.mark_unknown()


def summarize_session(words: List[models.Word]) -> Tuple[int, int]:
    new_words = [w for w in words if w.familiarity_score == 0 or w.last_review_date is None]
    return len(words), len(new_words)
