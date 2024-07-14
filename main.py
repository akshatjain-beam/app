# app.main.py

from fastapi import FastAPI
from app.routers import items
from app.models import database

app = FastAPI()

app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Hello!"}

@app.on_event("startup")
async def init_db():
    database.Base.metadata.create_all(bind=database.engine)
