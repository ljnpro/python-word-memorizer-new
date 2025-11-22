from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.services import review as review_service
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return RedirectResponse(url="/review/today")


@router.get("/review/today", response_class=HTMLResponse)
def review_today(request: Request, db: Session = Depends(get_db)):
    words = review_service.get_today_review_words(db)
    return templates.TemplateResponse(
        "review.html",
        {
            "request": request,
            "words": words,
            "today": date.today(),
        },
    )


@router.post("/review/answer")
def review_answer(
    word_id: int = Form(...),
    known: bool = Form(...),
    db: Session = Depends(get_db),
):
    word: models.Word | None = db.query(models.Word).filter(models.Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    review_service.apply_review_action(word, known)
    db.add(word)
    db.commit()
    return {"status": "ok", "next_review_date": word.next_review_date}


@router.get("/review/summary", response_class=HTMLResponse)
def review_summary(request: Request, db: Session = Depends(get_db)):
    words = review_service.get_today_review_words(db)
    total, new_count = review_service.summarize_session(words)
    return templates.TemplateResponse(
        "summary.html",
        {"request": request, "total": total, "new_count": new_count, "today": date.today()},
    )
