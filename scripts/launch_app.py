#!/usr/bin/env python3
"""Launch Auto Sanación Studio background server (if needed) and open browser."""

from __future__ import annotations

import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SERVER_SCRIPT = PROJECT_ROOT / "webapp" / "server.py"
LOG_FILE = PROJECT_ROOT / "data" / "server.log"
HOST = "127.0.0.1"
PORT = 8795
HEALTH_URL = f"http://{HOST}:{PORT}/api/health"


def is_server_up() -> bool:
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(HEALTH_URL, timeout=1.0) as resp:
            if resp.status != 200:
                return False
            return b"Auto Sanaci" in resp.read()
    except Exception:
        return False


def ensure_server_running() -> None:
    if is_server_up():
        return
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    log_handle = LOG_FILE.open("a", encoding="utf-8")
    subprocess.Popen(
        [sys.executable, str(SERVER_SCRIPT)],
        cwd=str(PROJECT_ROOT),
        stdout=log_handle,
        stderr=log_handle,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )
    for _ in range(25):
        if is_server_up():
            return
        time.sleep(0.2)


def main() -> None:
    route = sys.argv[1] if len(sys.argv) > 1 else "/admin"
    if not route.startswith("/"):
        route = "/" + route
    ensure_server_running()
    webbrowser.open(f"http://{HOST}:{PORT}{route}")


if __name__ == "__main__":
    main()
