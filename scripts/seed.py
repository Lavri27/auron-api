from app.db.session import SessionLocal
from app.models.artist import Artist
from app.models.album import Album
from app.models.track import Track


db = SessionLocal()

artist = Artist(name="Test Artist")
db.add(artist)
db.commit()
db.refresh(artist)

album = Album(title="Test Album", artist_id=artist.id)
db.add(album)
db.commit()
db.refresh(album)

track = Track(
    title="Test Track",
    artist_id=artist.id,
    album_id=album.id,
    duration_sec=180,
)
db.add(track)
db.commit()

print("Seed data created")
