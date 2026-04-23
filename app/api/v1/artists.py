from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.models.artist import Artist
from app.schemas.artist import ArtistCreate, ArtistUpdate, ArtistRead
from app.utils.pagination import paginate

router = APIRouter()


def _serialize_paginated(query, limit: int, offset: int, schema):
    data = paginate(query, limit, offset)
    data["items"] = [schema.model_validate(item).model_dump() for item in data["items"]]
    return data


@router.get("/")
def list_artists(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    query = db.query(Artist).order_by(Artist.id.desc())
    return _serialize_paginated(query, limit, offset, ArtistRead)


@router.post("/", response_model=ArtistRead)
def create_artist(
    data: ArtistCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    artist = Artist(**data.model_dump())
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


@router.get("/{artist_id}", response_model=ArtistRead)
def get_artist(
    artist_id: int,
    db: Session = Depends(get_db),
):
    artist = db.get(Artist, artist_id)
    if not artist:
        raise HTTPException(404, "Artist not found")
    return artist


@router.patch("/{artist_id}", response_model=ArtistRead)
def update_artist(
    artist_id: int,
    data: ArtistUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    artist = db.get(Artist, artist_id)
    if not artist:
        raise HTTPException(404, "Artist not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(artist, k, v)

    db.commit()
    db.refresh(artist)
    return artist


@router.delete("/{artist_id}")
def delete_artist(
    artist_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    artist = db.get(Artist, artist_id)
    if not artist:
        raise HTTPException(404, "Artist not found")

    db.delete(artist)
    db.commit()
    return {"status": "deleted"}
