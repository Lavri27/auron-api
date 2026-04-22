from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/listen/{track_id}", response_class=HTMLResponse)
def listen_page(track_id: int):
    html = """<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Загрузка плеера…</title>
  <style>
    :root {
      color-scheme: dark;
      --bg-1: #090b11;
      --bg-2: #0f1420;
      --card: rgba(18, 23, 34, 0.84);
      --card-2: rgba(255, 255, 255, 0.04);
      --text: #f5f7fb;
      --muted: #98a3b7;
      --border: rgba(255, 255, 255, 0.09);
      --accent: #7c9cff;
      --accent-2: #9c7cff;
      --danger: #ffb4b4;
      --shadow: 0 28px 100px rgba(0, 0, 0, 0.45);
      --radius: 26px;
    }

    * { box-sizing: border-box; }

    html, body {
      margin: 0;
      min-height: 100%;
    }

    body {
      min-height: 100vh;
      display: grid;
      place-items: center;
      background:
        radial-gradient(circle at top, rgba(124, 156, 255, 0.18), transparent 34%),
        radial-gradient(circle at bottom right, rgba(156, 124, 255, 0.12), transparent 28%),
        linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%);
      color: var(--text);
      font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      padding: 28px;
    }

    .shell {
      width: min(100%, 980px);
      display: grid;
      gap: 18px;
    }

    .card {
      display: grid;
      grid-template-columns: minmax(280px, 420px) minmax(0, 1fr);
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
      backdrop-filter: blur(18px);
      box-shadow: var(--shadow);
    }

    .cover-wrap {
      position: relative;
      min-height: 320px;
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0));
      overflow: hidden;
    }

    .cover-wrap::after {
      content: "";
      position: absolute;
      inset: auto 0 0 0;
      height: 42%;
      background: linear-gradient(180deg, rgba(5, 7, 12, 0) 0%, rgba(5, 7, 12, 0.72) 100%);
      pointer-events: none;
    }

    .cover {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      background: #0a0c10;
    }

    .cover-badge {
      position: absolute;
      left: 18px;
      bottom: 18px;
      z-index: 1;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(12, 16, 25, 0.62);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: #dbe5ff;
      font-size: 13px;
      backdrop-filter: blur(10px);
    }

    .content {
      display: flex;
      flex-direction: column;
      padding: 28px;
      gap: 20px;
    }

    .eyebrow {
      font-size: 12px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--muted);
    }

    .header h1 {
      margin: 0;
      font-size: clamp(28px, 5vw, 42px);
      line-height: 1.05;
      letter-spacing: -0.03em;
    }

    .meta {
      margin-top: 10px;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.5;
    }

    .player-panel {
      display: grid;
      gap: 16px;
      padding: 18px;
      border-radius: 22px;
      background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.025));
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
    }

    audio {
      display: none;
    }

    .transport {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .play-btn {
      width: 68px;
      height: 68px;
      border-radius: 50%;
      border: 0;
      cursor: pointer;
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: white;
      box-shadow: 0 14px 36px rgba(124, 156, 255, 0.35);
      display: grid;
      place-items: center;
      transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.18s ease;
    }

    .play-btn:hover { transform: translateY(-1px) scale(1.01); }
    .play-btn:active { transform: scale(0.98); }

    .play-btn svg {
      width: 26px;
      height: 26px;
      fill: currentColor;
      margin-left: 2px;
    }

    .play-btn.is-playing svg {
      margin-left: 0;
    }

    .transport-main {
      min-width: 0;
      flex: 1;
    }

    .now-playing {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
    }

    .now-playing strong {
      display: block;
      font-size: 15px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .now-playing span {
      color: var(--muted);
      font-size: 13px;
      white-space: nowrap;
    }

    .timeline {
      display: grid;
      gap: 8px;
    }

    .time-row {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: 13px;
      font-variant-numeric: tabular-nums;
    }

    input[type="range"] {
      -webkit-appearance: none;
      appearance: none;
      width: 100%;
      height: 6px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.12);
      outline: none;
      cursor: pointer;
    }

    input[type="range"]::-webkit-slider-runnable-track {
      height: 6px;
      border-radius: 999px;
      background: transparent;
    }

    input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #fff;
      border: 0;
      margin-top: -5px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.28);
    }

    input[type="range"]::-moz-range-track {
      height: 6px;
      border-radius: 999px;
      background: transparent;
    }

    input[type="range"]::-moz-range-thumb {
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #fff;
      border: 0;
      box-shadow: 0 4px 14px rgba(0,0,0,0.28);
    }

    .controls-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }

    .stack {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      min-width: 180px;
    }

    .stack label {
      color: var(--muted);
      font-size: 13px;
      white-space: nowrap;
    }

    .stack select {
      border: 1px solid rgba(255,255,255,0.09);
      background: rgba(255,255,255,0.05);
      color: var(--text);
      border-radius: 12px;
      padding: 10px 12px;
      font: inherit;
      outline: none;
    }

    .links {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .links a {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 11px 14px;
      border-radius: 14px;
      text-decoration: none;
      color: #d7e2ff;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.07);
      transition: background 0.18s ease, transform 0.18s ease;
    }

    .links a:hover {
      background: rgba(255,255,255,0.07);
      transform: translateY(-1px);
    }

    .status {
      color: var(--muted);
      font-size: 14px;
      min-height: 20px;
    }

    .error {
      color: var(--danger);
    }

    .hint {
      color: var(--muted);
      font-size: 13px;
    }

    @media (max-width: 820px) {
      .card {
        grid-template-columns: 1fr;
      }

      .cover-wrap {
        min-height: 260px;
        aspect-ratio: 1 / 1;
      }

      .content {
        padding: 20px;
      }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="card">
      <div class="cover-wrap">
        <img id="cover" class="cover" alt="Обложка трека" />
        <div class="cover-badge">♪ Сейчас играет в Auron</div>
      </div>

      <div class="content">
        <div class="header">
          <div class="eyebrow">Auron Player</div>
          <h1 id="title">Загрузка…</h1>
          <div class="meta" id="meta">Получаем данные о треке</div>
        </div>

        <div class="player-panel">
          <audio id="player" preload="metadata"></audio>

          <div class="transport">
            <button id="playBtn" class="play-btn" type="button" aria-label="Воспроизвести">
              <svg id="playIcon" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"></path></svg>
            </button>

            <div class="transport-main">
              <div class="now-playing">
                <strong id="miniTitle">Загрузка трека…</strong>
                <span id="stateText">Готов к запуску</span>
              </div>

              <div class="timeline">
                <input id="seek" type="range" min="0" max="100" step="0.1" value="0" aria-label="Позиция воспроизведения" />
                <div class="time-row">
                  <span id="currentTime">0:00</span>
                  <span id="totalTime">0:00</span>
                </div>
              </div>
            </div>
          </div>

          <div class="controls-row">
            <div class="stack" style="flex: 1 1 220px;">
              <label for="volume">Громкость</label>
              <input id="volume" type="range" min="0" max="1" step="0.01" value="1" aria-label="Громкость" />
            </div>

            <div class="stack" style="justify-content: flex-end;">
              <label for="speed">Скорость</label>
              <select id="speed" aria-label="Скорость воспроизведения">
                <option value="0.75">0.75x</option>
                <option value="1" selected>1x</option>
                <option value="1.25">1.25x</option>
                <option value="1.5">1.5x</option>
                <option value="2">2x</option>
              </select>
            </div>
          </div>
        </div>

        <div class="links">
          <a id="stream-link" href="#" target="_blank" rel="noopener noreferrer">Открыть аудиопоток</a>
          <a id="api-link" href="#" target="_blank" rel="noopener noreferrer">Открыть JSON трека</a>
        </div>

        <p class="status" id="status"></p>
        <div class="hint">Плеер поддерживает перемотку, регулировку громкости и смену скорости.</div>
      </div>
    </section>
  </main>

  <script>
    const trackId = __TRACK_ID__;
    const titleEl = document.getElementById("title");
    const miniTitleEl = document.getElementById("miniTitle");
    const metaEl = document.getElementById("meta");
    const coverEl = document.getElementById("cover");
    const playerEl = document.getElementById("player");
    const playBtnEl = document.getElementById("playBtn");
    const playIconEl = document.getElementById("playIcon");
    const seekEl = document.getElementById("seek");
    const volumeEl = document.getElementById("volume");
    const speedEl = document.getElementById("speed");
    const currentTimeEl = document.getElementById("currentTime");
    const totalTimeEl = document.getElementById("totalTime");
    const stateTextEl = document.getElementById("stateText");
    const streamLinkEl = document.getElementById("stream-link");
    const apiLinkEl = document.getElementById("api-link");
    const statusEl = document.getElementById("status");

    const fallbackCover = "data:image/svg+xml;utf8," + encodeURIComponent(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200">
        <defs>
          <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0%" stop-color="#10131a" />
            <stop offset="100%" stop-color="#1e2640" />
          </linearGradient>
        </defs>
        <rect width="1200" height="1200" fill="url(#g)"/>
        <circle cx="600" cy="600" r="290" fill="#2b3657" opacity="0.85"/>
        <circle cx="600" cy="600" r="120" fill="#11151e"/>
        <text x="50%" y="88%" text-anchor="middle" fill="#c6d2f0" font-size="64" font-family="Arial, sans-serif">Auron</text>
      </svg>
    `);

    function mediaUrl(path) {
      if (!path) return fallbackCover;
      if (path.startsWith("http://") || path.startsWith("https://")) return path;
      return `/media/${path.replace(/^\\/+/, "")}`;
    }

    function formatTime(sec) {
      const value = Number(sec);
      if (!Number.isFinite(value) || value < 0) return "0:00";
      const total = Math.floor(value);
      const minutes = Math.floor(total / 60);
      const seconds = String(total % 60).padStart(2, "0");
      return `${minutes}:${seconds}`;
    }

    function setRangeFill(input, ratio) {
      const percent = Math.max(0, Math.min(100, ratio * 100));
      input.style.background = `linear-gradient(90deg, var(--accent) 0%, var(--accent-2) ${percent}%, rgba(255,255,255,0.12) ${percent}%, rgba(255,255,255,0.12) 100%)`;
    }

    function setPlayState(isPlaying) {
      playBtnEl.classList.toggle("is-playing", isPlaying);
      playBtnEl.setAttribute("aria-label", isPlaying ? "Пауза" : "Воспроизвести");
      playIconEl.innerHTML = isPlaying
        ? '<path d="M7 5h4v14H7zm6 0h4v14h-4z"></path>'
        : '<path d="M8 5v14l11-7z"></path>';
      stateTextEl.textContent = isPlaying ? "Играет" : "На паузе";
    }

    async function getJson(url) {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`${response.status} ${response.statusText}`);
      }
      return response.json();
    }

    async function togglePlayback() {
      if (!playerEl.src) return;
      try {
        if (playerEl.paused) {
          await playerEl.play();
        } else {
          playerEl.pause();
        }
      } catch (error) {
        statusEl.textContent = `Ошибка воспроизведения: ${String(error.message || error)}`;
      }
    }

    async function loadPage() {
      try {
        const track = await getJson(`/api/v1/tracks/${trackId}`);
        const artist = await getJson(`/api/v1/artists/${track.artist_id}`);
        const album = track.album_id ? await getJson(`/api/v1/albums/${track.album_id}`) : null;

        const streamUrl = `/api/v1/tracks/${trackId}/stream/content`;
        const coverPath = track.cover_path || (album && album.cover_path) || null;
        const duration = Number(track.duration_sec || 0);

        document.title = `${track.title} — ${artist.name}`;
        titleEl.textContent = track.title;
        miniTitleEl.textContent = track.title;
        metaEl.textContent = album ? `${artist.name} • ${album.title}` : artist.name;

        coverEl.src = mediaUrl(coverPath);
        coverEl.onerror = function () {
          coverEl.src = fallbackCover;
        };

        playerEl.src = streamUrl;
        streamLinkEl.href = streamUrl;
        apiLinkEl.href = `/api/v1/tracks/${trackId}`;
        totalTimeEl.textContent = formatTime(duration);
        statusEl.textContent = duration > 0 ? `Длительность: ${formatTime(duration)}` : "";

        setRangeFill(seekEl, 0);
        setRangeFill(volumeEl, Number(volumeEl.value));
      } catch (error) {
        document.title = "Ошибка загрузки";
        titleEl.textContent = "Не удалось открыть трек";
        miniTitleEl.textContent = "Ошибка загрузки";
        metaEl.innerHTML = `<span class="error">${String(error.message || error)}</span>`;
        coverEl.src = fallbackCover;
        statusEl.textContent = "Проверьте, существует ли track_id и загружены ли медиафайлы.";
      }
    }

    playBtnEl.addEventListener("click", togglePlayback);

    playerEl.addEventListener("play", () => setPlayState(true));
    playerEl.addEventListener("pause", () => setPlayState(false));
    playerEl.addEventListener("ended", () => {
      setPlayState(false);
      stateTextEl.textContent = "Воспроизведение завершено";
    });
    playerEl.addEventListener("waiting", () => {
      stateTextEl.textContent = "Буферизация…";
    });
    playerEl.addEventListener("loadedmetadata", () => {
      totalTimeEl.textContent = formatTime(playerEl.duration);
    });
    playerEl.addEventListener("timeupdate", () => {
      currentTimeEl.textContent = formatTime(playerEl.currentTime);
      const ratio = playerEl.duration ? playerEl.currentTime / playerEl.duration : 0;
      seekEl.value = String(ratio * 100);
      setRangeFill(seekEl, ratio);
    });

    seekEl.addEventListener("input", () => {
      const ratio = Number(seekEl.value) / 100;
      setRangeFill(seekEl, ratio);
      if (Number.isFinite(playerEl.duration) && playerEl.duration > 0) {
        playerEl.currentTime = ratio * playerEl.duration;
      }
    });

    volumeEl.addEventListener("input", () => {
      const volume = Number(volumeEl.value);
      playerEl.volume = volume;
      setRangeFill(volumeEl, volume);
    });

    speedEl.addEventListener("change", () => {
      playerEl.playbackRate = Number(speedEl.value);
    });

    document.addEventListener("keydown", (event) => {
      if (["INPUT", "SELECT", "TEXTAREA"].includes(document.activeElement?.tagName)) return;
      if (event.code === "Space") {
        event.preventDefault();
        togglePlayback();
      }
    });

    setPlayState(false);
    setRangeFill(seekEl, 0);
    setRangeFill(volumeEl, 1);
    loadPage();
  </script>
</body>
</html>
""".replace("__TRACK_ID__", str(track_id))

    return HTMLResponse(content=html)
