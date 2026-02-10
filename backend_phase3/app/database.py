"""
Database initialization module to handle model registration properly
"""
from sqlmodel import SQLModel
# Import models directly to avoid relative import issues
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Conversation, Message, Task  # Import all models to register them with SQLModel

# All models are now registered with SQLModel when this module is imported
__all__ = ["SQLModel", "Conversation", "Message", "Task"]