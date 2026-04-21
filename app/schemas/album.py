from datetime import date, datetime

from app.schemas.common import ORMModel


class AlbumCreate(ORMModel):
    artist_id: int
    title: str
    release_date: date | None = None


class AlbumUpdate(ORMModel):
    title: str | None = None
    release_date: date | None = None


class AlbumRead(ORMModel):
    id: int
    artist_id: int
    title: str
    cover_path: str | None
    release_date: date | None
    created_at: datetime
