from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config.settings import DATABASES_URL

engine = create_engine(DATABASES_URL)

SesionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()