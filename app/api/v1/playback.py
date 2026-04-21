from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.listening_history import ListeningHistory
from app.models.track import Track

router = APIRouter()


@router.post("/start/{track_id}")
def start_playback(
    track_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    track = db.get(Track, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    event = ListeningHistory(user_id=user.id, track_id=track_id)
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"message": "playback started", "history_id": event.id}


@router.post("/finish/{history_id}")
def finish_playback(
    history_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    event = db.get(ListeningHistory, history_id)
    if not event or event.user_id != user.id:
        raise HTTPException(status_code=404, detail="History entry not found")

    event.finished_at = datetime.utcnow()
    db.commit()
    return {"message": "playback finished"}
