from fastapi import File, Form, UploadFile
from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: int = Form(..., description="Unique user identifier")
    message: str = Form("", description="User message")
    files: list[UploadFile] = File(default=[], description="Files to upload")


class ChatResponse(BaseModel):
    response: str
