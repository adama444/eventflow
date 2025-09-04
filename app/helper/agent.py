import json
import re
import tempfile

from app.core.logger import get_logger
from app.helper.drive import upload_file_to_drive

logger = get_logger(__name__)


def extract_json_from_output(llm_output: str) -> dict | None:
    """
    Extract JSON object from LLM output string.
    Handles cases where LLM may include text before/after JSON.
    """
    logger.info("call: extract_json_from_output")
    try:
        match = re.search(
            r"(?:```json)?\s*(\{(?:.)*\})\s*(?:```)?", llm_output, re.DOTALL
        )
        if match:
            data = json.loads(match.group(1).strip())
            logger.info(f"data: {data}")
            return data
    except Exception as e:
        logger.error(f"Error extracting JSON: {e}")
    return None


def save_json_to_drive(json_data: dict, file_name: str) -> str | None:
    """Save a JSON object to Google Drive"""
    logger.info("call: save_json_to_drive")
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp:
        json.dump(json_data, tmp, indent=4, ensure_ascii=False)
        tmp.flush()
        file_url = upload_file_to_drive(file_path=tmp.name, file_name=file_name)
    return file_url
