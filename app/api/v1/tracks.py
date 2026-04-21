from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.models.track import Track
from app.schemas.track import TrackCreate, TrackUpdate, TrackRead, StreamResponse
from app.services.track_service import TrackService

router = APIRouter()


@router.get("/", response_model=dict)
def list_tracks(
    db: Session = Depends(get_db),
    limit: int = Query(20),
    offset: int = Query(0),
):
    return TrackService.list_public(db, limit, offset)


@router.post("/", response_model=TrackRead)
def create_track(
    data: TrackCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    return TrackService.create(db, data.model_dump())


@router.get("/{track_id}", response_model=TrackRead)
def get_track(track_id: int, db: Session = Depends(get_db)):
    track = TrackService.get(db, track_id)
    if not track:
        raise HTTPException(404, "Track not found")
    return track


@router.get("/{track_id}/stream", response_model=StreamResponse)
def stream_track(track_id: int, db: Session = Depends(get_db)):
    track = TrackService.get(db, track_id)
    if not track:
        raise HTTPException(404, "Track not found")

    return TrackService.get_stream(track)


@router.patch("/{track_id}", response_model=TrackRead)
def update_track(
    track_id: int,
    data: TrackUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    track = db.get(Track, track_id)
    if not track:
        raise HTTPException(404, "Track not found")

    return TrackService.update(
        db,
        track,
        data.model_dump(exclude_unset=True),
    )


@router.delete("/{track_id}")
def delete_track(
    track_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    track = db.get(Track, track_id)
    if not track:
        raise HTTPException(404, "Track not found")

    TrackService.delete(db, track)
    return {"status": "deleted"}
