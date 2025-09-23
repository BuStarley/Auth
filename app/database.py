from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from app.config import Config

engine = create_engine(Config().DATABASE_URL)
session = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

session().query(UserDB)