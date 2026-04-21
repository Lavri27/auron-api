from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.models.album import Album
from app.schemas.album import AlbumCreate, AlbumUpdate, AlbumRead
from app.utils.pagination import paginate

router = APIRouter()


@router.get("/", response_model=dict)
def list_albums(
    db: Session = Depends(get_db),
    limit: int = Query(20),
    offset: int = Query(0),
):
    query = db.query(Album).order_by(Album.id.desc())
    return paginate(query, limit, offset)


@router.post("/", response_model=AlbumRead)
def create_album(
    data: AlbumCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    album = Album(**data.model_dump())
    db.add(album)
    db.commit()
    db.refresh(album)
    return album


@router.get("/{album_id}", response_model=AlbumRead)
def get_album(album_id: int, db: Session = Depends(get_db)):
    album = db.get(Album, album_id)
    if not album:
        raise HTTPException(404, "Album not found")
    return album


@router.patch("/{album_id}", response_model=AlbumRead)
def update_album(
    album_id: int,
    data: AlbumUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    album = db.get(Album, album_id)
    if not album:
        raise HTTPException(404, "Album not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(album, k, v)

    db.commit()
    db.refresh(album)
    return album


@router.delete("/{album_id}")
def delete_album(
    album_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    album = db.get(Album, album_id)
    if not album:
        raise HTTPException(404, "Album not found")

    db.delete(album)
    db.commit()
    return {"status": "deleted"}
