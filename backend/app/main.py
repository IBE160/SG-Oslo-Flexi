from fastapi import FastAPI
from app.core.config import settings
from app.api import health, queue, orchestrator

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(health.router)
app.include_router(queue.router)
app.include_router(orchestrator.router, prefix="/orchestrator", tags=["orchestrator"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
