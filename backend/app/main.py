from fastapi import FastAPI
from app.core.config import settings
from app.api import health

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(health.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
