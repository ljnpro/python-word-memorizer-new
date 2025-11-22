from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import WordCreate, WordUpdate
from app.services import import_export

router = APIRouter(prefix="/words")

templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
def list_words(
    request: Request,
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None),
    sort: Optional[str] = Query("created_at"),
):
    query = db.query(models.Word)
    if search:
        like = f"%{search}%"
        query = query.filter(or_(models.Word.word.ilike(like), models.Word.meaning.ilike(like)))
    if sort == "alphabet":
        query = query.order_by(models.Word.word.asc())
    elif sort == "familiarity":
        query = query.order_by(models.Word.familiarity_score.desc(), models.Word.word.asc())
    else:
        query = query.order_by(models.Word.created_at.desc())
    words = query.all()
    return templates.TemplateResponse(
        "words.html",
        {"request": request, "words": words, "search": search or "", "sort": sort},
    )


@router.post("", response_class=HTMLResponse)
def create_word(
    request: Request,
    db: Session = Depends(get_db),
    word: str = Form(...),
    meaning: str = Form(...),
    phonetic: Optional[str] = Form(None),
    example: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
):
    if db.query(models.Word).filter(models.Word.word == word).first():
        raise HTTPException(status_code=400, detail="Word already exists")
    word_obj = models.Word(
        word=word.strip(),
        meaning=meaning.strip(),
        phonetic=phonetic.strip() if phonetic else None,
        example=example.strip() if example else None,
        tags=tags.strip() if tags else None,
        next_review_date=date.today(),
    )
    db.add(word_obj)
    db.commit()
    return PlainTextResponse("created", status_code=201)


@router.post("/{word_id}")
def update_word(
    word_id: int,
    db: Session = Depends(get_db),
    meaning: Optional[str] = Form(None),
    example: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    phonetic: Optional[str] = Form(None),
):
    word_obj = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not word_obj:
        raise HTTPException(status_code=404, detail="Word not found")
    if meaning is not None:
        word_obj.meaning = meaning
    if example is not None:
        word_obj.example = example
    if tags is not None:
        word_obj.tags = tags
    if phonetic is not None:
        word_obj.phonetic = phonetic
    db.commit()
    return PlainTextResponse("updated")


@router.post("/{word_id}/delete")
def delete_word(word_id: int, db: Session = Depends(get_db)):
    word_obj = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not word_obj:
        raise HTTPException(status_code=404, detail="Word not found")
    db.delete(word_obj)
    db.commit()
    return PlainTextResponse("deleted")


@router.post("/import")
async def import_words(db: Session = Depends(get_db), file: UploadFile = Form(...)):
    imported, skipped = await import_export.import_csv(db, file)
    return {"imported": imported, "skipped": skipped}


@router.get("/export")
def export_words(db: Session = Depends(get_db)):
    csv_content = import_export.export_csv(db)
    return PlainTextResponse(csv_content, media_type="text/csv")
