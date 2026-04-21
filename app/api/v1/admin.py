from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.models.album import Album
from app.models.artist import Artist
from app.models.track import Track
from app.services.storage_service import StorageService

router = APIRouter()


@router.post("/artists/{artist_id}/image")
def upload_artist_image(
    artist_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    artist = db.get(Artist, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    artist.image_path = StorageService.save_file(file, "covers")
    db.commit()
    return {"image_path": artist.image_path}


@router.post("/albums/{album_id}/cover")
def upload_album_cover(
    album_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    album = db.get(Album, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    album.cover_path = StorageService.save_file(file, "covers")
    db.commit()
    return {"cover_path": album.cover_path}


@router.post("/tracks/{track_id}/file")
def upload_track_file(
    track_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    track = db.get(Track, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    track.audio_path = StorageService.save_file(file, "tracks")
    db.commit()
    return {"audio_path": track.audio_path}
