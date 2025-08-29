from typing import Any, cast

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from langchain.schema import HumanMessage

from app.agents.agent import chatbot_app
from app.core.database import get_db_session
from app.helper.user import get_user
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter(prefix="/chat", tags=["Chatbot"])


@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db_session)):
    """Chat endpoint with conversation state persisted in PostgreSQL."""
    # Ensure user exists
    user = get_user(db, request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = chatbot_app.invoke(
        cast(Any, {"messages": [HumanMessage(request.message)]}),
        config={"configurable": {"thread_id": str(user.id)}},
    )
    ai_message = result["messages"][-1]

    return ChatResponse(response=ai_message.content)
