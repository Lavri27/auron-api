from sqlalchemy.orm import Session

from app.models.listening_history import ListeningHistory


class HistoryService:
    @staticmethod
    def list_user_history(db: Session, user_id: int) -> list[ListeningHistory]:
        return (
            db.query(ListeningHistory)
            .filter(ListeningHistory.user_id == user_id)
            .order_by(ListeningHistory.id.desc())
            .all()
        )
