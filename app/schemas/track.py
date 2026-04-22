from datetime import datetime

from app.schemas.common import ORMModel


class TrackCreate(ORMModel):
    artist_id: int
    album_id: int | None = None
    title: str
    duration_sec: int = 0


class TrackUpdate(ORMModel):
    title: str | None = None
    duration_sec: int | None = None
    is_public: bool | None = None


class TrackRead(ORMModel):
    id: int
    artist_id: int
    album_id: int | None
    title: str
    audio_path: str | None
    duration_sec: int
    is_public: bool
    created_at: datetime


class StreamResponse(ORMModel):
    track_id: int
    stream_url: str
    content_type: str
    content_length: int
    accept_ranges: str
    supports_seek: bool
