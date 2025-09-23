from fastapi import FastAPI
from app.database import create_engine, Base
from app.api import router

__name__ = "main"
app = FastAPI(tytle="User API")
app.include_router(router)

@app.get("/")
async def root():
    return {"Hello": "World"}