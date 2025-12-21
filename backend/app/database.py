# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import QueuePool
from app.config import settings


# -------------------------
# SQLAlchemy Base
# -------------------------
class Base(DeclarativeBase):
    """
    Base class for all ORM models.
    Alembic will reference this.
    """
    pass


# -------------------------
# Engine
# -------------------------
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,            # safe default for beta
    max_overflow=20,         # burst handling
    pool_timeout=30,
    pool_recycle=1800,       # avoid stale connections
    pool_pre_ping=True,     # auto-heal dropped DB connections
    echo=False,              # NEVER True in prod
    future=True,
)


# -------------------------
# Session Factory
# -------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# -------------------------
# FastAPI Dependency
# -------------------------
def get_db():
    """
    Dependency for DB session.
    Ensures:
    - One session per request
    - Proper cleanup
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
