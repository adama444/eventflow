# app/routers/chat.py
from typing import Any, cast
from fastapi import APIRouter
from app.schemas.event_data import ChatRequest, ChatResponse
from app.agents.event_agent import chatbot_app

router = APIRouter(prefix="/chat", tags=["Chatbot"])

# Keep a global state for now (later we’ll replace with checkpointed memory)
conversation_state:dict = {"messages": []}


@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    # Append user message
    conversation_state["messages"].append(request.message)

    # Run through LangGraph agent
    result = chatbot_app.invoke(cast(Any, conversation_state))

    # Extract last AI message
    ai_message = result["messages"][-1]

    return ChatResponse(response=ai_message, messages=result["messages"])
