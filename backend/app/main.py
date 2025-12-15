from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import health, queue, orchestrator, users, auth, documents, agents

app = FastAPI(title=settings.PROJECT_NAME)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # frontends allowed
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # allow all headers (including Content-Type)
)

app.include_router(health.router)
app.include_router(queue.router)
app.include_router(orchestrator.router, prefix="/orchestrator", tags=["orchestrator"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
