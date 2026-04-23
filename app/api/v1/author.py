from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_author, get_db
from app.models.album import Album
from app.models.artist import Artist
from app.models.track import Track
from app.models.user import User
from app.schemas.album import AlbumCreate, AlbumRead, AlbumUpdate
from app.schemas.artist import ArtistCreate, ArtistRead, ArtistUpdate
from app.schemas.track import TrackCreate, TrackRead, TrackUpdate
from app.services.storage_service import StorageService
from app.utils.pagination import paginate

router = APIRouter()


def _serialize_paginated(query, limit: int, offset: int, schema):
    data = paginate(query, limit, offset)
    data["items"] = [schema.model_validate(item).model_dump() for item in data["items"]]
    return data


def _get_author_artist_or_403(db: Session, artist_id: int, user: User) -> Artist:
    artist = db.get(Artist, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    if not (user.is_admin or artist.owner_user_id == user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return artist


def _get_author_track_or_403(db: Session, track_id: int, user: User) -> Track:
    track = db.get(Track, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    artist = db.get(Artist, track.artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    if not (user.is_admin or artist.owner_user_id == user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return track


def _get_author_album_or_403(db: Session, album_id: int, user: User) -> Album:
    album = db.get(Album, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    artist = db.get(Artist, album.artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    if not (user.is_admin or artist.owner_user_id == user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return album


@router.get("/me")
def author_me(user: User = Depends(get_current_author)):
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_author": user.is_author,
        "is_admin": user.is_admin,
    }


@router.get("/artists")
def list_my_artists(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    query = db.query(Artist).order_by(Artist.id.desc())
    if not user.is_admin:
        query = query.filter(Artist.owner_user_id == user.id)
    return _serialize_paginated(query, limit, offset, ArtistRead)


@router.post("/artists", response_model=ArtistRead)
def create_my_artist(
    data: ArtistCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
):
    artist = Artist(
        name=data.name,
        bio=data.bio,
        owner_user_id=user.id,
    )
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


@router.patch("/artists/{artist_id}", response_model=ArtistRead)
def update_my_artist(
    artist_id: int,
    data: ArtistUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
):
    artist = _get_author_artist_or_403(db, artist_id, user)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(artist, key, value)

    db.commit()
    db.refresh(artist)
    return artist


@router.post("/artists/{artist_id}/image")
def upload_my_artist_image(
    artist_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
):
    artist = _get_author_artist_or_403(db, artist_id, user)
    artist.image_path = StorageService.save_file(file, "covers")
    db.commit()
    return {"image_path": artist.image_path}


@router.get("/albums")
def list_my_albums(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    query = db.query(Album).join(Artist, Album.artist_id == Artist.id).order_by(Album.id.desc())
    if not user.is_admin:
        query = query.filter(Artist.owner_user_id == user.id)
    return _serialize_paginated(query, limit, offset, AlbumRead)


@router.post("/albums", response_model=AlbumRead)
def create_my_album(
    data: AlbumCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
):
    _get_author_artist_or_403(db, data.artist_id, user)

    album = Album(
        artist_id=data.artist_id,
        title=data.title,
        release_date=data.release_date,
    )
    db.add(album)
    db.commit()
    db.refresh(album)
    return album


@router.patch("/albums/{album_id}", response_model=AlbumRead)
def update_my_album(
    album_id: int,
    data: AlbumUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
):
    album = _get_author_album_or_403(db, album_id, user)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(album, key, value)

    db.commit()
    db.refresh(album)
    return album


@router.post("/albums/{album_id}/cover")
def upload_my_album_cover(
    album_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
):
    album = _get_author_album_or_403(db, album_id, user)
    album.cover_path = StorageService.save_file(file, "covers")
    db.commit()
    return {"cover_path": album.cover_path}


@router.get("/tracks")
def list_my_tracks(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    query = db.query(Track).join(Artist, Track.artist_id == Artist.id).order_by(Track.id.desc())
    if not user.is_admin:
        query = query.filter(Artist.owner_user_id == user.id)
    return _serialize_paginated(query, limit, offset, TrackRead)


@router.post("/tracks", response_model=TrackRead)
def create_my_track(
    data: TrackCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
):
    _get_author_artist_or_403(db, data.artist_id, user)

    track = Track(
        artist_id=data.artist_id,
        album_id=data.album_id,
        title=data.title,
        description=data.description,
        genre=data.genre,
        duration_sec=data.duration_sec,
        is_public=False,
        is_published=False,
    )
    db.add(track)
    db.commit()
    db.refresh(track)
    return track


@router.patch("/tracks/{track_id}", response_model=TrackRead)
def update_my_track(
    track_id: int,
    data: TrackUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
):
    track = _get_author_track_or_403(db, track_id, user)

    update_data = data.model_dump(exclude_unset=True)

    if "artist_id" in update_data:
        update_data.pop("artist_id")

    if "album_id" in update_data and update_data["album_id"] is not None:
        album = db.get(Album, update_data["album_id"])
        if not album:
            raise HTTPException(status_code=404, detail="Album not found")
        artist = db.get(Artist, album.artist_id)
        if not artist or (not user.is_admin and artist.owner_user_id != user.id):
            raise HTTPException(status_code=403, detail="Not enough permissions")

    for key, value in update_data.items():
        setattr(track, key, value)

    db.commit()
    db.refresh(track)
    return track


@router.post("/tracks/{track_id}/file")
def upload_my_track_file(
    track_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
):
    track = _get_author_track_or_403(db, track_id, user)
    track.audio_path = StorageService.save_file(file, "tracks")
    db.commit()
    return {"audio_path": track.audio_path}


@router.post("/tracks/{track_id}/cover")
def upload_my_track_cover(
    track_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
):
    track = _get_author_track_or_403(db, track_id, user)
    track.cover_path = StorageService.save_file(file, "covers")
    db.commit()
    return {"cover_path": track.cover_path}


@router.post("/tracks/{track_id}/publish", response_model=TrackRead)
def publish_my_track(
    track_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
):
    track = _get_author_track_or_403(db, track_id, user)

    if not track.audio_path:
        raise HTTPException(status_code=400, detail="Upload audio file before publishing")

    track.is_published = True
    track.is_public = True
    db.commit()
    db.refresh(track)
    return track


@router.post("/tracks/{track_id}/unpublish", response_model=TrackRead)
def unpublish_my_track(
    track_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_author),
):
    track = _get_author_track_or_403(db, track_id, user)
    track.is_published = False
    track.is_public = False
    db.commit()
    db.refresh(track)
    return track
