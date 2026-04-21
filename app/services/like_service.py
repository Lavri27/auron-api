from sqlalchemy.orm import Session

from app.models.liked_track import LikedTrack
from app.models.track import Track


class LikeService:
    @staticmethod
    def list_user_likes(db: Session, user_id: int) -> list[LikedTrack]:
        return (
            db.query(LikedTrack)
            .filter(LikedTrack.user_id == user_id)
            .order_by(LikedTrack.id.desc())
            .all()
        )

    @staticmethod
    def add_like(db: Session, user_id: int, track_id: int) -> LikedTrack:
        track = db.get(Track, track_id)
        if not track:
            raise ValueError("Track not found")

        existing = (
            db.query(LikedTrack)
            .filter(LikedTrack.user_id == user_id, LikedTrack.track_id == track_id)
            .first()
        )
        if existing:
            return existing

        like = LikedTrack(user_id=user_id, track_id=track_id)
        db.add(like)
        db.commit()
        db.refresh(like)
        return like

    @staticmethod
    def remove_like(db: Session, user_id: int, track_id: int) -> None:
        like = (
            db.query(LikedTrack)
            .filter(LikedTrack.user_id == user_id, LikedTrack.track_id == track_id)
            .first()
        )
        if like:
            db.delete(like)
            db.commit()
