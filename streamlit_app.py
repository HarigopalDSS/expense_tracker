from __future__ import annotations

import importlib.util
import runpy
import socket
import threading
import time
from pathlib import Path

import uvicorn

BASE_DIR = Path(__file__).resolve().parent
BACKEND_FILE = BASE_DIR / "backend.py" / "models.py" / "mainn.py"
FRONTEND_FILE = BASE_DIR / "backend.py" / "models.py" / "app.py"


def _port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex((host, port)) == 0


def _load_backend_app():
    spec = importlib.util.spec_from_file_location("expense_backend", BACKEND_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load backend module from {BACKEND_FILE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "app"):
        raise RuntimeError("Backend module does not expose `app`")
    return module.app


def _start_backend() -> None:
    # Streamlit Cloud runs one process, so start FastAPI in a daemon thread.
    if _port_open("127.0.0.1", 8000):
        return

    backend_app = _load_backend_app()
    config = uvicorn.Config(
        app=backend_app,
        host="127.0.0.1",
        port=8000,
        log_level="warning",
    )
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    for _ in range(30):
        if _port_open("127.0.0.1", 8000):
            return
        time.sleep(0.2)


_start_backend()
runpy.run_path(str(FRONTEND_FILE), run_name="__main__")
