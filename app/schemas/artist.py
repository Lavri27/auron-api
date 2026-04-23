from datetime import datetime

from app.schemas.common import ORMModel


class ArtistCreate(ORMModel):
    name: str
    bio: str | None = None


class ArtistUpdate(ORMModel):
    name: str | None = None
    bio: str | None = None


class ArtistRead(ORMModel):
    id: int
    owner_user_id: int | None
    name: str
    bio: str | None
    image_path: str | None
    created_at: datetime
