from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.schemas.playlist import PlaylistCreate, PlaylistRead
from app.services.playlist_service import PlaylistService

router = APIRouter()


@router.get("/", response_model=list[PlaylistRead])
def list_my_playlists(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return PlaylistService.list_user_playlists(db, user.id)


@router.post("/", response_model=PlaylistRead, status_code=status.HTTP_201_CREATED)
def create_playlist(
    payload: PlaylistCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return PlaylistService.create(db, user.id, payload)


@router.get("/{playlist_id}", response_model=PlaylistRead)
def get_playlist(
    playlist_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    playlist = PlaylistService.get_user_playlist(db, user.id, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist


@router.post("/{playlist_id}/tracks/{track_id}", response_model=PlaylistRead)
def add_track_to_playlist(
    playlist_id: int,
    track_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    playlist = PlaylistService.get_user_playlist(db, user.id, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    try:
        return PlaylistService.add_track(db, playlist, track_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.delete("/{playlist_id}/tracks/{track_id}", response_model=PlaylistRead)
def remove_track_from_playlist(
    playlist_id: int,
    track_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    playlist = PlaylistService.get_user_playlist(db, user.id, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    try:
        return PlaylistService.remove_track(db, playlist, track_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist(
    playlist_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    playlist = PlaylistService.get_user_playlist(db, user.id, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    PlaylistService.delete(db, playlist)
