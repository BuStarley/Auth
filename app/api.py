from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from hashlib import sha256
from models import UserDB

router = APIRouter()

@router.get("/users", response_model=List[UserDB])
async def get_users(db: Session = Depends(get_db)):
    return db.query().all()

@router.post("/register")
async def register_user(user: UserDB, db: Session = Depends(get_db)):
    if db.query().filter_by(email=user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user.id = db.query().count() + 1
    user.password = sha256(user.password.encode()).hexdigest()
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully", "user": user}