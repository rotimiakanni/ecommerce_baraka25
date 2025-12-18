from fastapi import FastAPI
from app.api.v1 import auth
from app.core.config import settings


app = FastAPI(title="FastAPI E-commerce")


app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI E-commerce!"}
