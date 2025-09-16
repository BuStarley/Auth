from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from hasher import Hasher
from database import get_db
from models import UserDB

router = APIRouter()

@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()

@router.post("/register")
async def register_user(user_data: UserDB, db: Session = Depends(get_db)):
    if db.query(UserDB).filter(UserDB.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = UserDB(**user_data.dict())
    new_user.password = Hasher(user_data.password).hash()
    new_user.id = db.query(UserDB).count() + 1
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
