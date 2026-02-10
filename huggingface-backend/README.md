---
title: Todo API Backend
emoji: 🚀
colorFrom: purple
colorTo: yellow
sdk: docker
hf_hub_id: sufyan-repo/todo-backend
pinned: false
---

# Todo API Backend

This is a FastAPI-based backend for the Todo application with PostgreSQL database support.

## Features

- FastAPI framework
- PostgreSQL database with asyncpg
- SQLModel ORM
- Authentication and authorization
- CRUD operations for todos
- Health check endpoint

## Endpoints

- `/health` - Health check endpoint
- `/api/auth/*` - Authentication endpoints
- `/api/tasks/*` - Task management endpoints

## Configuration

The application expects the following environment variable:
- `DATABASE_URL` - PostgreSQL database URL (format: postgresql://user:password@host:port/database)

## Deployment

This backend is deployed using Hugging Face Spaces with Docker runtime.