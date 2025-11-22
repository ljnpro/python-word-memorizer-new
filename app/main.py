from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import models
from app.database import engine
from app.routers import review, words

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Word Memorizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(review.router)
app.include_router(words.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
