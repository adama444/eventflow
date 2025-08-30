import mimetypes
import certifi
import httplib2
from google.oauth2 import service_account
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from googleapiclient.http import MediaFileUpload  # type: ignore

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

httplib2.CA_CERTS = certifi.where()  # type: ignore

SERVICE_ACCOUNT_FILE = settings.google_drive_credentials
DRIVE_FOLDER_ID = settings.drive_folder_id
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.file",
]


def create_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=credentials)
    return service


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
                supportsAllDrives=True,
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
