import time
from collections import defaultdict

RATE_LIMIT = 100  # запросов
WINDOW = 60       # секунд

requests = defaultdict(list)


def check_rate_limit(ip: str):
    now = time.time()
    window_start = now - WINDOW

    requests[ip] = [t for t in requests[ip] if t > window_start]

    if len(requests[ip]) >= RATE_LIMIT:
        return False

    requests[ip].append(now)
    return True
