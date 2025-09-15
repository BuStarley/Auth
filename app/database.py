from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import Config

engine = create_engine(Config().DATABASE_URL)
session = sessionmaker(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()