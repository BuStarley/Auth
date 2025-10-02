from fastapi import FastAPI
from app.database import engine, Base
from app.api import router

__name__ = "main"

Base.metadata.create_all(bind=engine)
app = FastAPI(tytle="User API")
app.include_router(router)

@app.get("/")
async def root():
    return {"Hello": "World"}