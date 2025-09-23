from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from hasher import Hasher
from database import get_db
from models import UserDB
from schemas import UserCreate, UserResponse

router = APIRouter()
hasher = Hasher()

@router.get("/users", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserDB).filter(UserDB.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = UserDB(
        email=user_data.email,
        password=hasher.hash_password(user_data.password),
        name=user_data.name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
