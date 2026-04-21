from datetime import datetime

from app.schemas.common import ORMModel


class HistoryRead(ORMModel):
    id: int
    user_id: int
    track_id: int
    started_at: datetime
    finished_at: datetime | None
