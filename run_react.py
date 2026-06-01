import subprocess
import sys
import time
import webbrowser
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"
PYTHON = ROOT / ".uv-venv" / "Scripts" / "python.exe"


def start_process(command, cwd):
    return subprocess.Popen(
        command,
        cwd=cwd,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )


def main():
    backend_python = PYTHON if PYTHON.exists() else Path(sys.executable)
    backend = start_process(
        [
            str(backend_python),
            "-m",
            "uvicorn",
            "fast_app:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        ROOT,
    )
    frontend = start_process(
        [
            "npm.cmd",
            "run",
            "dev",
            "--",
            "--host",
            "127.0.0.1",
            "--port",
            "5173",
        ],
        FRONTEND,
    )

    time.sleep(2)
    webbrowser.open_new("http://127.0.0.1:5173")

    try:
        while True:
            if backend.poll() is not None:
                return backend.returncode
            if frontend.poll() is not None:
                return frontend.returncode
            time.sleep(1)
    except KeyboardInterrupt:
        backend.terminate()
        frontend.terminate()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
