"""Desktop launcher: start FastAPI server and open a native window via pywebview."""
from __future__ import annotations

import socket
import threading
import time

import uvicorn
import webview

HOST = "127.0.0.1"
PORT = 8000


def _wait_for_server(host: str, port: int, timeout: float = 10.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            if sock.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.2)
    return False


def _serve_api(log_level: str = "warning") -> None:
    config = uvicorn.Config(
        "app.main:app", host=HOST, port=PORT, reload=False, log_level=log_level
    )
    server = uvicorn.Server(config)
    server.run()


def launch_gui(log_level: str = "warning") -> None:
    server_thread = threading.Thread(target=_serve_api, kwargs={"log_level": log_level}, daemon=True)
    server_thread.start()

    _wait_for_server(HOST, PORT, timeout=15.0)

    webview.create_window(
        "Word Memorizer",
        f"http://{HOST}:{PORT}/review/today",
        width=1200,
        height=800,
        resizable=True,
    )
    webview.start()


if __name__ == "__main__":
    launch_gui()
