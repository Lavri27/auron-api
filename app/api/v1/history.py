from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.services.history_service import HistoryService

router = APIRouter()


@router.get("/")
def list_history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return HistoryService.list_user_history(db, user.id)
