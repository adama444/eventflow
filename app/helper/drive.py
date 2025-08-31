import mimetypes
import os

import certifi
import httplib2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from googleapiclient.http import MediaFileUpload  # type: ignore

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

httplib2.CA_CERTS = certifi.where()  # type: ignore

OAUTH_CLIENT_FILE = settings.google_drive_credentials
TOKEN_FILE = settings.google_oauth_token
DRIVE_FOLDER_ID = settings.drive_folder_id
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.file",
]


def create_drive_service():
    """
    Create a Google Drive service using OAuth2 user credentials.
    Handles first-time authentication and token refresh automatically.
    """

    creds = None

    # Load saved token (if exists)
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials, authenticate via browser
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                logger.error(f"Failed to refresh token: {e}")
                creds = None
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    OAUTH_CLIENT_FILE, SCOPES
                )
                creds = flow.run_local_server(port=0)
            except Exception as e:
                logger.error(f"OAuth authentication failed: {e}")
                raise

        # Save the new token
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def upload_file_to_drive(
    file_path: str, file_name: str, drive_folder_id: str = DRIVE_FOLDER_ID
) -> str | None:
    """
    Upload a file to Google Drive and return its public URL.

    Args:
        file_path (str): Local path of the file to upload
        file_name (str): Custom name for the file in Drive
        drive_folder_id (str): Drive folder ID where the file should be stored

    Returns:
        str: URL of the uploaded file
    """

    service = create_drive_service()

    mime_type, _ = mimetypes.guess_type(file_path)

    file_metadata = {"name": file_name, "parents": [drive_folder_id]}

    try:
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
        uploaded_file = (
            service.files()
            .create(
                body=file_metadata,
                media_body=media,
                fields="webViewLink",
            )
            .execute()
        )

        return uploaded_file.get("webViewLink")
    except HttpError as e:
        logger.error(f"Google API Error: {e}")
        return None
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return None
