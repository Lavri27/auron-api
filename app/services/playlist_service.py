from sqlalchemy.orm import Session

from app.models.playlist import Playlist
from app.models.track import Track
from app.schemas.playlist import PlaylistCreate


class PlaylistService:
    @staticmethod
    def list_user_playlists(db: Session, user_id: int) -> list[Playlist]:
        return (
            db.query(Playlist)
            .filter(Playlist.user_id == user_id)
            .order_by(Playlist.id.desc())
            .all()
        )

    @staticmethod
    def create(db: Session, user_id: int, payload: PlaylistCreate) -> Playlist:
        playlist = Playlist(
            user_id=user_id,
            title=payload.title,
            description=payload.description,
        )
        db.add(playlist)
        db.commit()
        db.refresh(playlist)
        return playlist

    @staticmethod
    def get_user_playlist(db: Session, user_id: int, playlist_id: int) -> Playlist | None:
        return (
            db.query(Playlist)
            .filter(Playlist.id == playlist_id, Playlist.user_id == user_id)
            .first()
        )

    @staticmethod
    def add_track(db: Session, playlist: Playlist, track_id: int) -> Playlist:
        track = db.get(Track, track_id)
        if not track:
            raise ValueError("Track not found")

        if track not in playlist.tracks:
            playlist.tracks.append(track)
            db.commit()
            db.refresh(playlist)

        return playlist

    @staticmethod
    def remove_track(db: Session, playlist: Playlist, track_id: int) -> Playlist:
        track = db.get(Track, track_id)
        if not track:
            raise ValueError("Track not found")

        if track in playlist.tracks:
            playlist.tracks.remove(track)
            db.commit()
            db.refresh(playlist)

        return playlist

    @staticmethod
    def delete(db: Session, playlist: Playlist) -> None:
        db.delete(playlist)
        db.commit()
