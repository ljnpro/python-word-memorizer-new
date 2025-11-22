from pathlib import Path

from platformdirs import user_data_dir
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


def _build_database_url() -> str:
    data_dir = Path(user_data_dir("WordMemorizer", "WordMemorizer"))
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = data_dir / "wordmemorizer.db"
    return f"sqlite:///{db_path}"


DATABASE_URL = _build_database_url()

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
