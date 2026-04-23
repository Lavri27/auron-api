from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.album import Album
from app.models.artist import Artist
from app.models.track import Track
from app.schemas.album import AlbumRead
from app.schemas.artist import ArtistRead
from app.schemas.track import TrackRead

router = APIRouter()


@router.get("/")
def search(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    tracks = (
        db.query(Track)
        .filter(
            Track.is_public.is_(True),
            Track.is_published.is_(True),
            Track.title.ilike(f"%{q}%"),
        )
        .limit(20)
        .all()
    )

    artists = (
        db.query(Artist)
        .filter(Artist.name.ilike(f"%{q}%"))
        .limit(20)
        .all()
    )

    albums = (
        db.query(Album)
        .filter(Album.title.ilike(f"%{q}%"))
        .limit(20)
        .all()
    )

    return {
        "query": q,
        "tracks": [TrackRead.model_validate(t).model_dump() for t in tracks],
        "artists": [ArtistRead.model_validate(a).model_dump() for a in artists],
        "albums": [AlbumRead.model_validate(a).model_dump() for a in albums],
    }
