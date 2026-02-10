from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api import tasks, auth, chat

from contextlib import asynccontextmanager
from .db import create_db_and_tables
from .models.user import User
from .models.task import Task
from .models.conversation import Conversation, Message  # Import models to register them with SQLModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"]
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log full traceback to server stdout for debugging
    traceback.print_exception(type(exc), exc, exc.__traceback__)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )

app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api/tasks")
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

# Phase 3: AI Chatbot extension added
