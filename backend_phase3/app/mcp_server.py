import asyncio
from sqlmodel import Session, select
from typing import Dict, Any, List, Optional
import json

# We'll import the models inside the functions to avoid import conflicts at module level
# This is a workaround for the circular import issue

from .db import engine


class TodoMCPHandler:
    def __init__(self):
        # This class will now use database operations instead of in-memory storage
        pass

    async def add_task(self, title: str, description: Optional[str] = None, user_id: str = "default") -> Dict[str, Any]:
        """Add a new task for the user"""
        with Session(engine) as session:
            # Import locally to avoid circular import issues
            from ..models import Task
            new_task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=False
            )
            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            return {
                "success": True,
                "task": {
                    "id": new_task.id,
                    "user_id": new_task.user_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "completed": new_task.completed
                },
                "message": f"Task '{title}' added successfully"
            }

    async def list_tasks(self, user_id: str = "default", status: Optional[str] = None) -> Dict[str, Any]:
        """List tasks for the user, optionally filtered by status"""
        with Session(engine) as session:
            # Import locally to avoid circular import issues
            from ..models import Task
            statement = select(Task).where(Task.user_id == user_id)

            if status == "completed":
                statement = statement.where(Task.completed == True)
            elif status == "pending":
                statement = statement.where(Task.completed == False)

            results = session.exec(statement)
            tasks = results.all()

            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                })

            return {
                "tasks": task_list,
                "count": len(task_list),
                "message": f"Found {len(task_list)} tasks"
            }

    async def complete_task(self, task_id: int, user_id: str = "default") -> Dict[str, Any]:
        """Mark a task as completed"""
        with Session(engine) as session:
            # Import locally to avoid circular import issues
            from ..models import Task
            # Find the task by ID and user
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = session.exec(statement)
            task = result.first()

            if not task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found for user {user_id}"
                }

            task.completed = True
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                },
                "message": f"Task '{task.title}' marked as completed"
            }

    async def delete_task(self, task_id: int, user_id: str = "default") -> Dict[str, Any]:
        """Delete a task"""
        with Session(engine) as session:
            # Import locally to avoid circular import issues
            from ..models import Task
            # Find the task by ID and user
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = session.exec(statement)
            task = result.first()

            if not task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found for user {user_id}"
                }

            session.delete(task)
            session.commit()

            return {
                "success": True,
                "message": f"Task '{task.title}' deleted successfully"
            }

    async def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
                         completed: Optional[bool] = None, user_id: str = "default") -> Dict[str, Any]:
        """Update a task"""
        with Session(engine) as session:
            # Import locally to avoid circular import issues
            from ..models import Task
            # Find the task by ID and user
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = session.exec(statement)
            task = result.first()

            if not task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found for user {user_id}"
                }

            # Update fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if completed is not None:
                task.completed = completed

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                },
                "message": f"Task '{task.title}' updated successfully"
            }


# Initialize the handler
handler = TodoMCPHandler()