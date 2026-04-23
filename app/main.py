from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import admin, albums, artists, auth, author, history, likes, playback, playlists, search, tracks
from app.core.config import settings
from app.web.smoke_player import router as smoke_player_router

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory=settings.storage_path), name="media")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(author.router, prefix="/api/v1/author", tags=["author"])
app.include_router(artists.router, prefix="/api/v1/artists", tags=["artists"])
app.include_router(albums.router, prefix="/api/v1/albums", tags=["albums"])
app.include_router(tracks.router, prefix="/api/v1/tracks", tags=["tracks"])
app.include_router(playlists.router, prefix="/api/v1/playlists", tags=["playlists"])
app.include_router(likes.router, prefix="/api/v1/likes", tags=["likes"])
app.include_router(history.router, prefix="/api/v1/history", tags=["history"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(playback.router, prefix="/api/v1/playback", tags=["playback"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

app.include_router(smoke_player_router, tags=["smoke"])


@app.get("/health")
def health():
    return {"status": "ok"}
