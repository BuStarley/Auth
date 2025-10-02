from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.hasher import Hasher
from app.database import get_db
from app.models import UserDB
from app.schemas import UserCreate, UserResponse, UserUpdate


router = APIRouter()
hasher = Hasher()


@router.get("/users", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()


@router.get("/users/{id}", response_model=list[UserResponse])
async def get_users(id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{id}", response_model=UserResponse)
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(UserDB(id=id))
    db.commit()
    return db_user


@router.put("/users/{id}", response_model=UserResponse)
async def update_user(user_data: UserUpdate, id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    new_data = UserDB(
        email=db_user.email,
        password=hasher.hash_password(user_data.password),
        user_name=db_user.user_name)

    db.add(new_data)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/users", response_model=UserResponse)
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
