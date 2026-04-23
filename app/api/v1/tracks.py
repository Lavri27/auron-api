from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.models.track import Track
from app.schemas.track import StreamResponse, TrackCreate, TrackRead, TrackUpdate
from app.services.track_service import TrackService

router = APIRouter()


def _serialize_paginated(data):
    data["items"] = [TrackRead.model_validate(item).model_dump() for item in data["items"]]
    return data


@router.get("/")
def list_tracks(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    data = TrackService.list_public(db, limit, offset)
    return _serialize_paginated(data)


@router.post("/", response_model=TrackRead)
def create_track(
    data: TrackCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    payload = data.model_dump()
    payload.setdefault("is_public", True)
    payload.setdefault("is_published", True)
    return TrackService.create(db, payload)


@router.get("/{track_id}", response_model=TrackRead)
def get_track(track_id: int, db: Session = Depends(get_db)):
    track = TrackService.get_public(db, track_id)
    if not track:
        raise HTTPException(404, "Track not found")
    return track


@router.get("/{track_id}/stream", response_model=StreamResponse)
def get_track_stream_info(track_id: int, db: Session = Depends(get_db)):
    track = TrackService.get_public(db, track_id)
    if not track:
        raise HTTPException(404, "Track not found")
    return TrackService.get_stream(track)


@router.head("/{track_id}/stream/content", status_code=200)
def head_track_stream(track_id: int, db: Session = Depends(get_db)):
    track = TrackService.get_public(db, track_id)
    if not track:
        raise HTTPException(404, "Track not found")
    return TrackService.stream_head(track)


@router.get("/{track_id}/stream/content")
def stream_track_content(
    track_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    track = TrackService.get_public(db, track_id)
    if not track:
        raise HTTPException(404, "Track not found")
    return TrackService.stream_content(request, track)


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
