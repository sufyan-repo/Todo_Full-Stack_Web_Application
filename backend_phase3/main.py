from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.db import engine
from app.routes import chat
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Phase 3 AI Chatbot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.on_event("startup")
async def startup():
    # Create database tables - models will be registered when routes are imported
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Phase 3 AI Chatbot API"}