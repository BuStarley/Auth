from fastapi import FastAPI

__name__ = "main"
app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "World"}