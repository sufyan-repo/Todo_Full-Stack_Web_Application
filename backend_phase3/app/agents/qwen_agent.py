import json
from typing import Dict, Any, List
# Import handler inside the functions to avoid circular import issues
def get_handler():
    from ..mcp_server import handler
    return handler


class QwenAgent:
    def __init__(self):
        self.tools = {
            "add_task": self._add_task,
            "list_tasks": self._list_tasks,
            "complete_task": self._complete_task,
            "delete_task": self._delete_task,
            "update_task": self._update_task
        }

    async def process_request(self, user_input: str, user_id: str, chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Process the user's request using Qwen-like logic
        """
        # Simple intent detection based on keywords
        user_input_lower = user_input.lower()

        # Determine intent
        if any(word in user_input_lower for word in ["add", "create", "new", "make"]):
            return await self._handle_add_task(user_input, user_id)
        elif any(word in user_input_lower for word in ["list", "show", "view", "see", "my"]):
            return await self._handle_list_tasks(user_input, user_id)
        elif any(word in user_input_lower for word in ["complete", "done", "finish", "mark"]):
            return await self._handle_complete_task(user_input, user_id)
        elif any(word in user_input_lower for word in ["delete", "remove", "cancel"]):
            return await self._handle_delete_task(user_input, user_id)
        elif any(word in user_input_lower for word in ["update", "change", "edit", "modify"]):
            return await self._handle_update_task(user_input, user_id)
        else:
            # Default response for unrecognized intents
            return {
                "response": f"I understand you said: '{user_input}'. I can help you manage your tasks. You can ask me to add, list, complete, delete, or update tasks.",
                "tool_calls": []
            }

    async def _extract_task_info(self, user_input: str) -> Dict[str, str]:
        """
        Extract task information from user input
        This is a simple implementation - in a real scenario, this would use NLP
        """
        # Remove common phrases
        user_input = user_input.lower().strip()

        # Look for keywords that might indicate task info
        if "add" in user_input or "create" in user_input:
            # Extract everything after common phrases
            for phrase in ["add ", "create ", "make ", "new "]:
                if phrase in user_input:
                    title = user_input.split(phrase)[1].strip()
                    # Look for description indicators
                    if "with description" in title or "and description" in title:
                        parts = title.split("with description") if "with description" in title else title.split("and description")
                        title = parts[0].strip()
                        description = parts[1].strip() if len(parts) > 1 else ""
                        return {"title": title, "description": description}
                    else:
                        return {"title": title, "description": ""}

        return {"title": "", "description": ""}

    async def _extract_task_id(self, user_input: str) -> int:
        """
        Extract task ID from user input
        This is a simple implementation - in a real scenario, this would use NLP
        """
        import re
        # Look for numbers in the input which might be task IDs
        numbers = re.findall(r'\d+', user_input)
        if numbers:
            return int(numbers[0])
        return 0  # Return 0 if no number found

    async def _handle_add_task(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Handle adding a task"""
        task_info = await self._extract_task_info(user_input)

        if not task_info["title"]:
            # Try to extract title from the input more directly
            parts = user_input.split()
            # Skip common verbs and get the rest as title
            skip_words = ["please", "can", "you", "add", "create", "make", "a", "an", "the", "to", "for"]
            title_parts = [word for word in parts if word.lower() not in skip_words]
            task_info["title"] = " ".join(title_parts).strip(" .!?")

        if task_info["title"]:
            handler = get_handler()
            result = await handler.add_task(task_info["title"], task_info["description"], user_id)

            if result["success"]:
                return {
                    "response": f"Successfully added task: {result['task']['title']}",
                    "tool_calls": [{
                        "name": "add_task",
                        "arguments": {
                            "title": task_info["title"],
                            "description": task_info["description"],
                            "user_id": user_id
                        },
                        "result": result
                    }]
                }
            else:
                return {
                    "response": f"Failed to add task: {result['message']}",
                    "tool_calls": []
                }
        else:
            return {
                "response": "I couldn't understand what task you want to add. Please specify the task title.",
                "tool_calls": []
            }

    async def _handle_list_tasks(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Handle listing tasks"""
        # Check if user wants specific status
        status = None
        user_input_lower = user_input.lower()
        if "completed" in user_input_lower:
            status = "completed"
        elif "pending" in user_input_lower or "incomplete" in user_input_lower:
            status = "pending"

        handler = get_handler()
        result = await handler.list_tasks(user_id, status)

        if result["count"] > 0:
            task_list = "\n".join([f"- {task['id']}: {task['title']}" +
                                  (f" ({'COMPLETED' if task['completed'] else 'PENDING'})" if task['completed'] else "")
                                  for task in result["tasks"]])
            response = f"Here are your tasks:\n{task_list}"
        else:
            response = "You don't have any tasks."

        return {
            "response": response,
            "tool_calls": [{
                "name": "list_tasks",
                "arguments": {
                    "user_id": user_id,
                    "status": status
                },
                "result": result
            }]
        }

    async def _handle_complete_task(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Handle completing a task"""
        task_id = await self._extract_task_id(user_input)

        if task_id > 0:
            handler = get_handler()
            result = await handler.complete_task(task_id, user_id)

            if result["success"]:
                return {
                    "response": f"Successfully completed task: {result['task']['title']}",
                    "tool_calls": [{
                        "name": "complete_task",
                        "arguments": {
                            "task_id": task_id,
                            "user_id": user_id
                        },
                        "result": result
                    }]
                }
            else:
                return {
                    "response": f"Failed to complete task: {result['message']}",
                    "tool_calls": []
                }
        else:
            return {
                "response": "I couldn't identify which task to complete. Please specify the task number.",
                "tool_calls": []
            }

    async def _handle_delete_task(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Handle deleting a task"""
        task_id = await self._extract_task_id(user_input)

        if task_id > 0:
            handler = get_handler()
            result = await handler.delete_task(task_id, user_id)

            if result["success"]:
                return {
                    "response": result["message"],
                    "tool_calls": [{
                        "name": "delete_task",
                        "arguments": {
                            "task_id": task_id,
                            "user_id": user_id
                        },
                        "result": result
                    }]
                }
            else:
                return {
                    "response": f"Failed to delete task: {result['message']}",
                    "tool_calls": []
                }
        else:
            return {
                "response": "I couldn't identify which task to delete. Please specify the task number.",
                "tool_calls": []
            }

    async def _handle_update_task(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Handle updating a task"""
        # This is a simplified implementation
        # In a real scenario, we'd need more sophisticated NLP to extract what to update
        task_id = await self._extract_task_id(user_input)

        if task_id > 0:
            # For now, we'll just say we need more information
            return {
                "response": f"I can help you update task #{task_id}. Please specify what you'd like to change (title, description, or completion status).",
                "tool_calls": []
            }
        else:
            return {
                "response": "I couldn't identify which task to update. Please specify the task number.",
                "tool_calls": []
            }

    async def _add_task(self, **kwargs) -> Dict[str, Any]:
        """Wrapper for MCP add_task function"""
        return await handler.add_task(**kwargs)

    async def _list_tasks(self, **kwargs) -> Dict[str, Any]:
        """Wrapper for MCP list_tasks function"""
        return await handler.list_tasks(**kwargs)

    async def _complete_task(self, **kwargs) -> Dict[str, Any]:
        """Wrapper for MCP complete_task function"""
        return await handler.complete_task(**kwargs)

    async def _delete_task(self, **kwargs) -> Dict[str, Any]:
        """Wrapper for MCP delete_task function"""
        return await handler.delete_task(**kwargs)

    async def _update_task(self, **kwargs) -> Dict[str, Any]:
        """Wrapper for MCP update_task function"""
        return await handler.update_task(**kwargs)