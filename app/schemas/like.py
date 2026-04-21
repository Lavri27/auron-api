from datetime import datetime

from app.schemas.common import ORMModel


class LikeRead(ORMModel):
    id: int
    user_id: int
    track_id: int
    created_at: datetime
