from fastapi import APIRouter
from models import User

router = APIRouter()

users = [User(name="<NAME>", email="<EMAIL>", password="<PASSWORD>")]

@router.get("/users")
async def get_users():
    return users