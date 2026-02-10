# Phase 3: AI-Powered Todo Assistant

This extension adds AI chatbot capabilities to the Phase 2 Todo application, allowing users to manage their tasks through natural language conversations.

## Architecture

The Phase 3 system consists of:
- **Backend**: FastAPI server with MCP tools for AI agent integration
- **Frontend**: Next.js chat interface using OpenAI ChatKit
- **Database**: Neon PostgreSQL storing conversations and messages
- **AI Agent**: Qwen-inspired logic for processing natural language requests

## Features

- Natural language task management (add, list, complete, delete, update tasks)
- Conversation history stored in database
- MCP tools for standardized AI integration
- Clean, responsive chat interface

## Prerequisites

- Python 3.9+
- Node.js 18+
- Neon PostgreSQL database
- Environment variables configured

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend_phase3
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in a `.env` file:
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_db
```

4. Run database migrations:
```bash
python migrate.py
```

5. Start the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend_phase3
```

2. Install JavaScript dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## API Endpoints

- `POST /api/{user_id}/chat` - Send a message to the AI chatbot
- `GET /api/{user_id}/history` - Get conversation history

## MCP Tools

The system exposes the following MCP tools for AI agent integration:

- `add_task` - Add a new task
- `list_tasks` - List tasks for a user
- `complete_task` - Mark a task as completed
- `delete_task` - Delete a task
- `update_task` - Update a task

## Usage

1. Access the chat interface at `http://localhost:3000`
2. The system will generate a user ID automatically
3. Type natural language requests like:
   - "Add a task to buy groceries"
   - "Show my tasks"
   - "Complete task #1"
   - "Delete task #2"

## Database Schema

- `conversations` table stores conversation metadata
- `messages` table stores individual messages in conversations

## Development

The Phase 3 system extends Phase 2 without modifying its core functionality. All new features are contained within the `backend_phase3` and `frontend_phase3` directories.

## Tech Stack

- Backend: Python, FastAPI, SQLModel, asyncpg
- Frontend: Next.js, React, Tailwind CSS
- Database: Neon PostgreSQL
- AI Integration: MCP (Model Context Protocol)
- Language Model: Qwen-inspired agent logic