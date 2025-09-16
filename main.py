from fastapi import FastAPI
from app.api import router

__name__ = "main"
app = FastAPI()
app.include_router(router)

@app.get("/")
async def root():
    return {"Hello": "World"}