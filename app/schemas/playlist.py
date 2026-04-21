from datetime import datetime

from app.schemas.common import ORMModel
from app.schemas.track import TrackRead


class PlaylistCreate(ORMModel):
    title: str
    description: str | None = None


class PlaylistRead(ORMModel):
    id: int
    user_id: int
    title: str
    description: str | None
    created_at: datetime
    tracks: list[TrackRead] = []
