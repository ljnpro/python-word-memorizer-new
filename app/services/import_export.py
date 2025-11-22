import csv
from datetime import date
from io import StringIO
from typing import Tuple

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app import models


async def import_csv(db: Session, file: UploadFile) -> Tuple[int, int]:
    content = await file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(StringIO(text))
    imported = 0
    skipped = 0
    for row in reader:
        word_text = (row.get("word") or "").strip()
        meaning = (row.get("meaning") or "").strip()
        if not word_text or not meaning:
            skipped += 1
            continue
        existing = db.query(models.Word).filter(models.Word.word == word_text).first()
        if existing:
            skipped += 1
            continue
        word = models.Word(
            word=word_text,
            meaning=meaning,
            phonetic=(row.get("phonetic") or "").strip() or None,
            example=(row.get("example") or "").strip() or None,
            tags=(row.get("tags") or "").strip() or None,
            next_review_date=date.today(),
        )
        db.add(word)
        imported += 1
    db.commit()
    return imported, skipped


def export_csv(db: Session) -> str:
    output = StringIO()
    fieldnames = ["word", "meaning", "phonetic", "example", "tags", "familiarity_score", "last_review_date", "next_review_date"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for word in db.query(models.Word).order_by(models.Word.word.asc()).all():
        writer.writerow(
            {
                "word": word.word,
                "meaning": word.meaning,
                "phonetic": word.phonetic or "",
                "example": word.example or "",
                "tags": word.tags or "",
                "familiarity_score": word.familiarity_score,
                "last_review_date": word.last_review_date or "",
                "next_review_date": word.next_review_date or "",
            }
        )
    return output.getvalue()
