from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from datetime import datetime
import json
from ..models import Message, Conversation
from ..db import engine
from ..agents.qwen_agent import QwenAgent
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: str

class ChatResponse(BaseModel):
    response: str
    tool_calls: List[dict] = []

@router.post("/{user_id}/chat")
async def chat(user_id: str, request: ChatRequest):
    # Create or get conversation
    with Session(engine) as session:
        # Check if conversation exists for this user
        statement = select(Conversation).where(Conversation.user_id == user_id)
        result = session.exec(statement)
        conversation = result.first()

        if not conversation:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Store user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        session.add(user_message)
        session.commit()

        # Get conversation history
        statement = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.timestamp)
        result = session.exec(statement)
        messages = result.all()

        # Convert messages to the format expected by the agent
        chat_history = []
        for msg in messages:
            chat_history.append({
                "role": msg.role,
                "content": msg.content
            })

        # Call the Qwen agent
        agent = QwenAgent()
        response = await agent.process_request(request.message, request.user_id, chat_history)

        # Store assistant response
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=response.get("response", ""),
            tool_calls=json.dumps(response.get("tool_calls", [])) if response.get("tool_calls") else None
        )
        session.add(assistant_message)
        session.commit()

        return ChatResponse(
            response=response.get("response", ""),
            tool_calls=response.get("tool_calls", [])
        )

@router.get("/{user_id}/history")
async def get_conversation_history(user_id: str):
    with Session(engine) as session:
        # Get conversation for user
        statement = select(Conversation).where(Conversation.user_id == user_id)
        result = session.exec(statement)
        conversation = result.first()

        if not conversation:
            return {"messages": []}

        # Get messages in conversation
        statement = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.timestamp)
        result = session.exec(statement)
        messages = result.all()

        return {
            "conversation_id": conversation.id,
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                } for msg in messages
            ]
        }