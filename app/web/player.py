from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/listen/{track_id}", response_class=HTMLResponse)
def listen_page(track_id: int):
    html = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Загрузка плеера…</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #0f1115;
      --card: #171a21;
      --text: #f3f5f7;
      --muted: #a7b0be;
      --border: #2a3040;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background: linear-gradient(180deg, #0b0d11 0%, #11151c 100%);
      color: var(--text);
      font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      padding: 24px;
    }}

    .card {{
      width: 100%;
      max-width: 460px;
      background: rgba(23, 26, 33, 0.95);
      border: 1px solid var(--border);
      border-radius: 22px;
      overflow: hidden;
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
      backdrop-filter: blur(12px);
    }}

    .cover-wrap {{
      aspect-ratio: 1 / 1;
      background: #0a0c10;
      display: grid;
      place-items: center;
      overflow: hidden;
    }}

    .cover {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      background: #0a0c10;
    }}

    .content {{
      padding: 20px;
    }}

    .eyebrow {{
      font-size: 12px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 10px;
    }}

    h1 {{
      margin: 0 0 8px;
      font-size: 28px;
      line-height: 1.15;
    }}

    .meta {{
      color: var(--muted);
      font-size: 15px;
      line-height: 1.5;
      margin-bottom: 18px;
    }}

    audio {{
      width: 100%;
      margin-top: 4px;
    }}

    .links {{
      margin-top: 16px;
      font-size: 14px;
      color: var(--muted);
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .links a {{
      color: #c7d7ff;
      text-decoration: none;
    }}

    .status {{
      color: var(--muted);
      font-size: 14px;
    }}

    .error {{
      color: #ffb4b4;
    }}
  </style>
</head>
<body>
  <main class="card">
    <div class="cover-wrap">
      <img id="cover" class="cover" alt="Обложка трека" />
    </div>

    <div class="content">
      <div class="eyebrow">Auron Player</div>
      <h1 id="title">Загрузка…</h1>
      <div class="meta" id="meta">Получаем данные о треке</div>

      <audio id="player" controls preload="metadata"></audio>

      <div class="links">
        <a id="stream-link" href="#" target="_blank" rel="noopener noreferrer">Открыть аудиопоток</a>
        <a id="api-link" href="#" target="_blank" rel="noopener noreferrer">Открыть JSON трека</a>
      </div>

      <p class="status" id="status"></p>
    </div>
  </main>

  <script>
    const trackId = {track_id};
    const titleEl = document.getElementById("title");
    const metaEl = document.getElementById("meta");
    const coverEl = document.getElementById("cover");
    const playerEl = document.getElementById("player");
    const streamLinkEl = document.getElementById("stream-link");
    const apiLinkEl = document.getElementById("api-link");
    const statusEl = document.getElementById("status");

    const fallbackCover = "data:image/svg+xml;utf8," + encodeURIComponent(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200">
        <rect width="1200" height="1200" fill="#0e1117"/>
        <circle cx="600" cy="600" r="300" fill="#1f2430"/>
        <circle cx="600" cy="600" r="120" fill="#0e1117"/>
        <text x="50%" y="88%" text-anchor="middle" fill="#9aa4b2" font-size="64" font-family="Arial, sans-serif">Auron</text>
      </svg>
    `);

    function mediaUrl(path) {{
      if (!path) return fallbackCover;
      if (path.startsWith("http://") || path.startsWith("https://")) return path;
      return `/media/${{path.replace(/^\\/+/, "")}}`;
    }}

    async function getJson(url) {{
      const response = await fetch(url);
      if (!response.ok) {{
        throw new Error(`${{response.status}} ${{response.statusText}}`);
      }}
      return response.json();
    }}

    async function loadPage() {{
      try {{
        const track = await getJson(`/api/v1/tracks/${{trackId}}`);
        const [artist, album] = await Promise.all([
          getJson(`/api/v1/artists/${{track.artist_id}}`),
          track.album_id ? getJson(`/api/v1/albums/${{track.album_id}}`) : Promise.resolve(null),
        ]);

        const streamUrl = `/api/v1/tracks/${{trackId}}/stream/content`;
        const coverPath = track.cover_path || (album && album.cover_path) || null;

        document.title = `${{track.title}} — ${{artist.name}}`;
        titleEl.textContent = track.title;
        metaEl.textContent = album
          ? `${{artist.name}} • ${{album.title}}`
          : artist.name;

        coverEl.src = mediaUrl(coverPath);
        coverEl.onerror = () => {{
          coverEl.src = fallbackCover;
        }};

        playerEl.src = streamUrl;
        streamLinkEl.href = streamUrl;
        apiLinkEl.href = `/api/v1/tracks/${{trackId}}`;

        const duration = Number(track.duration_sec || 0);
        const minutes = Math.floor(duration / 60);
        const seconds = String(duration % 60).padStart(2, "0");
        statusEl.textContent = duration > 0
          ? `Длительность: ${{minutes}}:${{seconds}}`
          : "";
      }} catch (error) {{
        document.title = "Ошибка загрузки";
        titleEl.textContent = "Не удалось открыть трек";
        metaEl.innerHTML = `<span class="error">${{String(error.message || error)}}</span>`;
        coverEl.src = fallbackCover;
        statusEl.textContent = "Проверьте, существует ли track_id и загружены ли медиафайлы.";
      }}
    }}

    loadPage();
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html)
