from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings


class StorageService:
    @staticmethod
    def save_file(upload: UploadFile, subdir: str) -> str:
        extension = ""
        if upload.filename and "." in upload.filename:
            extension = "." + upload.filename.rsplit(".", 1)[-1].lower()

        filename = f"{uuid4().hex}{extension}"
        base_dir = Path(settings.storage_path) / subdir
        base_dir.mkdir(parents=True, exist_ok=True)

        file_path = base_dir / filename
        with file_path.open("wb") as buffer:
            buffer.write(upload.file.read())

        return f"{subdir}/{filename}"
