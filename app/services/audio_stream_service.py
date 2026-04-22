import mimetypes
import re
from pathlib import Path

from fastapi import HTTPException, Request, status
from fastapi.responses import FileResponse, Response, StreamingResponse

from app.core.config import settings


class AudioStreamService:
    CHUNK_SIZE = 1024 * 1024  # 1 MB

    @classmethod
    def _resolve_audio_path(cls, audio_path: str) -> Path:
        base_dir = Path(settings.storage_path).resolve()
        file_path = (base_dir / audio_path).resolve()

        if not str(file_path).startswith(str(base_dir)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid audio path",
            )

        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Audio file not found",
            )

        return file_path

    @classmethod
    def _media_type(cls, file_path: Path) -> str:
        media_type, _ = mimetypes.guess_type(str(file_path))
        return media_type or "application/octet-stream"

    @classmethod
    def build_stream_info(cls, track_id: int, audio_path: str) -> dict:
        file_path = cls._resolve_audio_path(audio_path)
        file_size = file_path.stat().st_size

        return {
            "track_id": track_id,
            "stream_url": f"/api/v1/tracks/{track_id}/stream/content",
            "content_type": cls._media_type(file_path),
            "content_length": file_size,
            "accept_ranges": "bytes",
            "supports_seek": True,
        }

    @classmethod
    def head_response(cls, audio_path: str) -> Response:
        file_path = cls._resolve_audio_path(audio_path)
        file_size = file_path.stat().st_size
        media_type = cls._media_type(file_path)

        return Response(
            status_code=status.HTTP_200_OK,
            media_type=media_type,
            headers={
                "Accept-Ranges": "bytes",
                "Content-Length": str(file_size),
                "Cache-Control": "no-cache",
            },
        )

    @classmethod
    def stream(cls, request: Request, audio_path: str):
        file_path = cls._resolve_audio_path(audio_path)
        file_size = file_path.stat().st_size
        media_type = cls._media_type(file_path)
        range_header = request.headers.get("range")

        if not range_header:
            return FileResponse(
                path=file_path,
                media_type=media_type,
                filename=file_path.name,
                headers={
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(file_size),
                    "Cache-Control": "no-cache",
                },
            )

        start, end = cls._parse_range_header(range_header, file_size)
        content_length = end - start + 1

        def iter_file():
            with open(file_path, "rb") as file_obj:
                file_obj.seek(start)
                remaining = content_length

                while remaining > 0:
                    chunk_size = min(cls.CHUNK_SIZE, remaining)
                    chunk = file_obj.read(chunk_size)
                    if not chunk:
                        break
                    remaining -= len(chunk)
                    yield chunk

        return StreamingResponse(
            iter_file(),
            status_code=status.HTTP_206_PARTIAL_CONTENT,
            media_type=media_type,
            headers={
                "Accept-Ranges": "bytes",
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Content-Length": str(content_length),
                "Cache-Control": "no-cache",
            },
        )

    @classmethod
    def _parse_range_header(cls, range_header: str, file_size: int) -> tuple[int, int]:
        match = re.match(r"bytes=(\d*)-(\d*)$", range_header.strip())
        if not match:
            raise HTTPException(
                status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                detail="Invalid Range header",
                headers={"Content-Range": f"bytes */{file_size}"},
            )

        start_str, end_str = match.groups()

        if start_str == "" and end_str == "":
            raise HTTPException(
                status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                detail="Empty Range header",
                headers={"Content-Range": f"bytes */{file_size}"},
            )

        if start_str == "":
            suffix_length = int(end_str)
            if suffix_length <= 0:
                raise HTTPException(
                    status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                    detail="Invalid suffix range",
                    headers={"Content-Range": f"bytes */{file_size}"},
                )
            start = max(file_size - suffix_length, 0)
            end = file_size - 1
            return start, end

        start = int(start_str)
        end = int(end_str) if end_str else file_size - 1

        if start >= file_size or start < 0 or end < start:
            raise HTTPException(
                status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                detail="Range out of bounds",
                headers={"Content-Range": f"bytes */{file_size}"},
            )

        end = min(end, file_size - 1)
        return start, end
