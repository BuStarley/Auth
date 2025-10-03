from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.hasher import Hasher
from app.database import get_db
from app.models import UserDB
from app.schemas import UserRegister, UserResponse, UserUpdate, UserLogin, Token
from app.token import create_access_token, verify_token
from datetime import timedelta


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter()
hasher = Hasher()


@router.post("/auth/register", response_model=UserResponse)
async def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
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


@router.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/users", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()

@router.put("/auth/update/{id}", response_model=UserResponse)
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

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = verify_token(token)
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user:
        return False
    if not hasher.verify_password(password, user.password):
        return False
    return user