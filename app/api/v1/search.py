from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.artist import Artist
from app.models.track import Track

router = APIRouter()


@router.get("/")
def search(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    tracks = (
        db.query(Track)
        .filter(Track.is_public.is_(True), Track.title.ilike(f"%{q}%"))
        .limit(20)
        .all()
    )
    artists = (
        db.query(Artist)
        .filter(Artist.name.ilike(f"%{q}%"))
        .limit(20)
        .all()
    )
    return {
        "query": q,
        "tracks": tracks,
        "artists": artists,
    }
