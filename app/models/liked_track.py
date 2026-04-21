from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LikedTrack(Base):
    __tablename__ = "liked_tracks"
    __table_args__ = (
        UniqueConstraint("user_id", "track_id", name="uq_liked_tracks_user_track"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    track_id: Mapped[int] = mapped_column(ForeignKey("tracks.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
