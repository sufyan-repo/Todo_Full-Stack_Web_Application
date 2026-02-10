# MCP Tools Specification for Phase 3

## Overview
This document specifies the Model Context Protocol (MCP) tools available for the Phase 3 AI Chatbot. These tools enable the AI agent to perform todo management operations by exposing backend functionality through standardized interfaces.

## Available Tools

### 1. add_task
**Purpose**: Add a new task to the user's todo list

**Arguments**:
- `title` (string, required): The title of the task
- `description` (string, optional): Detailed description of the task
- `user_id` (string, required): Identifier of the user creating the task

**Returns**:
- `success` (boolean): Whether the operation was successful
- `task` (object): The created task object with id, title, description, completed status
- `message` (string): Human-readable confirmation message

**Example Usage**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "user_id": "user123"
}
```

### 2. list_tasks
**Purpose**: Retrieve a list of tasks for a specific user

**Arguments**:
- `user_id` (string, required): Identifier of the user whose tasks to retrieve
- `status` (string, optional): Filter by completion status ("completed", "pending", or null for all)

**Returns**:
- `tasks` (array): Array of task objects
- `count` (number): Total number of tasks returned
- `message` (string): Human-readable status message

**Example Usage**:
```json
{
  "user_id": "user123",
  "status": "pending"
}
```

### 3. complete_task
**Purpose**: Mark a specific task as completed

**Arguments**:
- `task_id` (number, required): The ID of the task to mark as complete
- `user_id` (string, required): Identifier of the user who owns the task

**Returns**:
- `success` (boolean): Whether the operation was successful
- `task` (object): The updated task object
- `message` (string): Human-readable confirmation message

**Example Usage**:
```json
{
  "task_id": 5,
  "user_id": "user123"
}
```

### 4. delete_task
**Purpose**: Remove a specific task from the user's list

**Arguments**:
- `task_id` (number, required): The ID of the task to delete
- `user_id` (string, required): Identifier of the user who owns the task

**Returns**:
- `success` (boolean): Whether the operation was successful
- `message` (string): Human-readable confirmation message

**Example Usage**:
```json
{
  "task_id": 3,
  "user_id": "user123"
}
```

### 5. update_task
**Purpose**: Modify an existing task

**Arguments**:
- `task_id` (number, required): The ID of the task to update
- `title` (string, optional): New title for the task
- `description` (string, optional): New description for the task
- `completed` (boolean, optional): New completion status for the task
- `user_id` (string, required): Identifier of the user who owns the task

**Returns**:
- `success` (boolean): Whether the operation was successful
- `task` (object): The updated task object
- `message` (string): Human-readable confirmation message

**Example Usage**:
```json
{
  "task_id": 7,
  "title": "Updated task title",
  "completed": true,
  "user_id": "user123"
}
```

## Implementation Notes
- All tools are stateless and rely on the database for persistence
- User authentication is handled at the API layer
- Tools return consistent response formats for easy parsing by AI agents
- Error handling is standardized across all tools