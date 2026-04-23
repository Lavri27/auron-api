"""
SMOKE / DEBUG PLAYER

Это не production frontend, а smoke-api-test страница для ручной проверки:

- audio streaming
- cover loading
- track title / metadata rendering
- player UI
- range requests / seek

Маршрут /listen/{track_id} сохранён специально для удобного тестирования.
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/listen/{track_id}", response_class=HTMLResponse)
def listen_page(track_id: int):
    return f"""
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Auron Smoke Player</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #0b0f14;
      --panel: #121821;
      --text: #ecf3ff;
      --muted: #9fb0c7;
      --line: rgba(255,255,255,0.08);
      --accent: #6ea8fe;
      --accent-2: #8b5cf6;
      --danger: #ff5d73;
      --shadow: 0 20px 60px rgba(0,0,0,0.35);
      --radius: 22px;
    }}

    * {{ box-sizing: border-box; }}

    html, body {{
      margin: 0;
      padding: 0;
      background:
        radial-gradient(circle at top left, rgba(110,168,254,0.16), transparent 28%),
        radial-gradient(circle at top right, rgba(139,92,246,0.16), transparent 24%),
        linear-gradient(180deg, #0b0f14 0%, #0c1118 100%);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      min-height: 100%;
    }}

    body {{ padding: 32px 18px 48px; }}

    .wrap {{
      width: min(1100px, 100%);
      margin: 0 auto;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(110,168,254,0.12);
      border: 1px solid rgba(110,168,254,0.25);
      color: #cfe0ff;
      font-size: 13px;
      letter-spacing: 0.02em;
      margin-bottom: 18px;
      backdrop-filter: blur(10px);
    }}

    .layout {{
      display: grid;
      grid-template-columns: 380px minmax(0, 1fr);
      gap: 24px;
      align-items: start;
    }}

    .card {{
      background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.02));
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow: hidden;
      backdrop-filter: blur(10px);
    }}

    .cover-card {{ padding: 18px; }}

    .cover-wrap {{
      position: relative;
      aspect-ratio: 1 / 1;
      border-radius: 18px;
      overflow: hidden;
      background: linear-gradient(135deg, #1b2330, #121821);
      border: 1px solid rgba(255,255,255,0.06);
    }}

    .cover {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}

    .meta-card {{ padding: 24px; }}

    .title {{
      margin: 0;
      font-size: clamp(28px, 5vw, 42px);
      line-height: 1.04;
      letter-spacing: -0.03em;
    }}

    .subtitle {{
      margin-top: 10px;
      color: var(--muted);
      font-size: 16px;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-top: 22px;
    }}

    .stat {{
      padding: 14px 16px;
      border-radius: 16px;
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.05);
    }}

    .stat-label {{
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}

    .stat-value {{
      font-size: 15px;
      color: var(--text);
      word-break: break-word;
    }}

    .player-block {{
      margin-top: 24px;
      padding: 18px;
      border-radius: 18px;
      background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.02));
      border: 1px solid rgba(255,255,255,0.06);
    }}

    audio {{
      width: 100%;
      margin-top: 10px;
      border-radius: 12px;
    }}

    .stream-link {{
      margin-top: 14px;
      color: var(--muted);
      font-size: 14px;
      word-break: break-all;
    }}

    .stream-link code {{
      display: inline-block;
      margin-top: 6px;
      padding: 8px 10px;
      border-radius: 10px;
      background: rgba(255,255,255,0.04);
      color: #dce8ff;
      border: 1px solid rgba(255,255,255,0.06);
    }}

    .error {{
      padding: 18px 20px;
      border-radius: 16px;
      background: rgba(255,93,115,0.08);
      border: 1px solid rgba(255,93,115,0.22);
      color: #ffd7de;
    }}

    .footer-note {{
      margin-top: 18px;
      color: var(--muted);
      font-size: 13px;
    }}

    .loading {{
      color: var(--muted);
      font-size: 15px;
    }}

    @media (max-width: 900px) {{
      .layout {{
        grid-template-columns: 1fr;
      }}
      .cover-card {{
        max-width: 560px;
      }}
    }}

    @media (max-width: 560px) {{
      body {{
        padding: 20px 12px 36px;
      }}
      .meta-card,
      .cover-card {{
        padding: 14px;
      }}
      .grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="badge">Smoke API Test · /listen/{track_id}</div>
    <div id="app" class="loading">Загрузка трека…</div>
    <div class="footer-note">
      Эта страница предназначена для ручной проверки streaming, metadata, cover loading и player UI.
    </div>
  </div>

  <script>
    const trackId = {track_id};

    function mediaUrl(path) {{
      if (!path) return null;
      if (path.startsWith("http://") || path.startsWith("https://")) return path;
      return `/media/${{path}}`;
    }}

    async function getJson(url) {{
      const response = await fetch(url);
      if (!response.ok) {{
        throw new Error(`HTTP ${{response.status}} for ${{url}}`);
      }}
      return response.json();
    }}

    async function tryGetJson(url) {{
      try {{
        return await getJson(url);
      }} catch (e) {{
        console.warn("Optional fetch failed:", url, e);
        return null;
      }}
    }}

    function fallbackCoverSvg(title = "Auron") {{
      const svg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" viewBox="0 0 1200 1200">
          <defs>
            <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
              <stop offset="0%" stop-color="#6ea8fe"/>
              <stop offset="100%" stop-color="#8b5cf6"/>
            </linearGradient>
          </defs>
          <rect width="1200" height="1200" rx="80" fill="#121821"/>
          <circle cx="600" cy="600" r="300" fill="url(#g)" opacity="0.95"/>
          <circle cx="600" cy="600" r="110" fill="#121821"/>
          <text x="600" y="1020" text-anchor="middle" fill="#dce8ff" font-family="Arial, sans-serif" font-size="72">${{title}}</text>
        </svg>
      `;
      return "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
    }}

    function safe(value, fallback = "—") {{
      return value ?? fallback;
    }}

    async function init() {{
      const app = document.getElementById("app");
      const streamUrl = `/api/v1/tracks/${{trackId}}/stream/content`;

      try {{
        const track = await getJson(`/api/v1/tracks/${{trackId}}`);
        const artist = await tryGetJson(`/api/v1/artists/${{track.artist_id}}`);
        const album = track.album_id ? await tryGetJson(`/api/v1/albums/${{track.album_id}}`) : null;

        const coverPath = track.cover_path || (album && album.cover_path) || null;
        const coverSrc = coverPath ? mediaUrl(coverPath) : fallbackCoverSvg(track.title || "Auron");

        document.title = artist?.name ? `${{track.title}} — ${{artist.name}}` : `${{track.title}} — Auron`;

        app.className = "";
        app.innerHTML = `
          <div class="layout">
            <section class="card cover-card">
              <div class="cover-wrap">
                <img class="cover" src="${{coverSrc}}" alt="Track cover" />
              </div>
            </section>

            <section class="card meta-card">
              <h1 class="title">${{track.title}}</h1>
              <div class="subtitle">
                ${{artist?.name || "Unknown artist"}}${{album ? ` · ${{album.title}}` : ""}}
              </div>

              <div class="grid">
                <div class="stat">
                  <div class="stat-label">Track ID</div>
                  <div class="stat-value">${{track.id}}</div>
                </div>
                <div class="stat">
                  <div class="stat-label">Artist ID</div>
                  <div class="stat-value">${{track.artist_id}}</div>
                </div>
                <div class="stat">
                  <div class="stat-label">Album</div>
                  <div class="stat-value">${{album ? album.title : "Single"}}</div>
                </div>
                <div class="stat">
                  <div class="stat-label">Duration</div>
                  <div class="stat-value">${{safe(track.duration_sec)}} sec</div>
                </div>
              </div>

              <div class="player-block">
                <div style="font-size:14px; color: var(--muted);">Streaming playback</div>
                <audio id="player" controls preload="metadata" src="${{streamUrl}}"></audio>

                <div class="stream-link">
                  Stream endpoint:
                  <br />
                  <code>${{streamUrl}}</code>
                </div>
              </div>
            </section>
          </div>
        `;

        const img = app.querySelector(".cover");
        img.addEventListener("error", () => {{
          img.src = fallbackCoverSvg(track.title || "Auron");
        }});

        const player = document.getElementById("player");
        player.addEventListener("error", () => {{
          const mediaError = player.error;
          console.error("Audio element error:", mediaError);
        }});
      }} catch (error) {{
        console.error(error);
        app.className = "";
        app.innerHTML = `
          <div class="error">
            Не удалось загрузить smoke player для track_id=${{trackId}}.<br />
            Причина: ${{error.message}}
          </div>
        `;
      }}
    }}

    init();
  </script>
</body>
</html>
"""
