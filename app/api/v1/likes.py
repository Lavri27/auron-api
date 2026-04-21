from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.schemas.like import LikeRead
from app.services.like_service import LikeService

router = APIRouter()


@router.get("/", response_model=list[LikeRead])
def list_my_likes(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return LikeService.list_user_likes(db, user.id)


@router.post("/{track_id}", response_model=LikeRead, status_code=status.HTTP_201_CREATED)
def add_like(
    track_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return LikeService.add_like(db, user.id, track_id)


@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_like(
    track_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    LikeService.remove_like(db, user.id, track_id)
