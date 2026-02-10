from sqlmodel import SQLModel
from models import Conversation, Message, Task
from app.db import engine

def run_migrations():
    """
    Run database migrations to create required tables
    """
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    run_migrations()