from fastapi import APIRouter, HTTPException
from models import User

router = APIRouter()

users = [User(name="<NAME>", email="<EMAIL>", password="<PASSWORD>", id=0)]

@router.get("/users")
async def get_users():
    return users

@router.post("/register")
async def register_user(user: User):
    if any(u.email == user.email for u in users):
        raise HTTPException(status_code=400, detail="Email already registered")
    user.id = len(users)
    users.append(user)
    return {"message": "User registered successfully"}