from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.track import Track
from app.utils.pagination import paginate


class TrackService:
    @staticmethod
    def create(db: Session, data: dict) -> Track:
        track = Track(**data)
        db.add(track)
        db.commit()
        db.refresh(track)
        return track

    @staticmethod
    def list_public(db: Session, limit: int, offset: int):
        query = db.query(Track).filter(Track.is_public.is_(True))
        return paginate(query, limit, offset)

    @staticmethod
    def get(db: Session, track_id: int) -> Track | None:
        return db.query(Track).filter(Track.id == track_id).first()

    @staticmethod
    def get_stream(track: Track):
        if not track.audio_path:
            raise ValueError("Track file not uploaded")

        return {
            "track_id": track.id,
            "stream_url": f"{settings.media_url}/{track.audio_path}",
        }

    @staticmethod
    def update(db: Session, track: Track, data: dict):
        for k, v in data.items():
            setattr(track, k, v)

        db.commit()
        db.refresh(track)
        return track

    @staticmethod
    def delete(db: Session, track: Track):
        db.delete(track)
        db.commit()
