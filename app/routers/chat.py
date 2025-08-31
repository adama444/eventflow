import os
from typing import Any, Iterable, cast
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from langchain.schema import HumanMessage

from app.agents.agent import chatbot_app
from app.core.config import settings
from app.core.database import get_db_session
from app.helper.drive import upload_file_to_drive
from app.helper.user import get_user
from app.schemas.chat import ChatRequest, ChatResponse

UPLOAD_DIR = "/tmp/eventflow"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_EXT = {"jpg", "jpeg", "png", "pdf", "docx"}

router = APIRouter(prefix="/chat", tags=["Chatbot"])


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest = Depends(), db: Session = Depends(get_db_session)
):
    """
    Chat endpoint that supports text and media files.
    - Text goes directly to the LLM
    - Files are uploaded to Google Drive, and their URLs are appended to the message
    """

    file_urls = []

    # Ensure user exists
    user = get_user(db, request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for file in request.files:
        ext = file.filename.split(".")[-1].lower()  # type: ignore[union-attr]

        if ext not in ALLOWED_EXT:
            raise HTTPException(
                status_code=400, detail=f"Not authorized file extension: '{ext}'"
            )

        filename = f"{uuid4()}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        try:
            with open(filepath, "wb") as f:
                f.write(await file.read())

            file_url = upload_file_to_drive(
                file_path=filepath,
                file_name=filename,
                drive_folder_id=settings.drive_media_folder_id,
            )

            file_urls.append(file_url)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    if file_urls:
        request.message += f"\nfiles url: {', '.join(file_urls)}"  # type: ignore[arg-type]

    result = chatbot_app.invoke(
        cast(Any, {"messages": [HumanMessage(request.message)]}),
        config={"configurable": {"thread_id": str(user.id)}},
    )
    ai_message = result["messages"][-1]

    return ChatResponse(response=ai_message.content)
