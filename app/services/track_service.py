from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session, joinedload

from app.models.track import Track
from app.services.audio_stream_service import AudioStreamService
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
        query = (
            db.query(Track)
            .options(joinedload(Track.artist), joinedload(Track.album))
            .filter(
                Track.is_public.is_(True),
                Track.is_published.is_(True),
            )
            .order_by(Track.id.desc())
        )
        return paginate(query, limit, offset)

    @staticmethod
    def get(db: Session, track_id: int) -> Track | None:
        return db.query(Track).filter(Track.id == track_id).first()

    @staticmethod
    def get_public(db: Session, track_id: int) -> Track | None:
        return (
            db.query(Track)
            .filter(
                Track.id == track_id,
                Track.is_public.is_(True),
                Track.is_published.is_(True),
            )
            .first()
        )

    @staticmethod
    def get_stream(track: Track):
        if not track.audio_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Track file not uploaded",
            )

        return AudioStreamService.build_stream_info(
            track_id=track.id,
            audio_path=track.audio_path,
        )

    @staticmethod
    def stream_content(request: Request, track: Track):
        if not track.audio_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Track file not uploaded",
            )

        return AudioStreamService.stream(request, track.audio_path)

    @staticmethod
    def stream_head(track: Track):
        if not track.audio_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Track file not uploaded",
            )

        return AudioStreamService.head_response(track.audio_path)

    @staticmethod
    def update(db: Session, track: Track, data: dict):
        for key, value in data.items():
            setattr(track, key, value)
        db.commit()
        db.refresh(track)
        return track

    @staticmethod
    def delete(db: Session, track: Track):
        db.delete(track)
        db.commit()
