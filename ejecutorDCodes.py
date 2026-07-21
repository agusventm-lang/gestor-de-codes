import json
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REPO_DIR = BASE_DIR / "repo_clone"
PID_FILE = BASE_DIR / ".repo_clone_pids.json"

EXCLUDE_DIRS = {"__pycache__", ".git"}


def find_python_scripts(repo_dir: Path):
    scripts = []
    for path in sorted(repo_dir.rglob("*.py")):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        if path.name == "__init__.py":
            continue
        scripts.append(path)
    return scripts


def load_previous_pids(pid_file: Path):
    if not pid_file.exists():
        return []

    try:
        with pid_file.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_pids(pid_file: Path, pids):
    try:
        with pid_file.open("w", encoding="utf-8") as f:
            json.dump(pids, f)
    except OSError:
        pass


def kill_process(pid: int):
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.kill(pid, subprocess.signal.SIGTERM)
    except Exception:
        pass


def kill_previous_processes(pid_file: Path):
    pids = load_previous_pids(pid_file)
    if not pids:
        return

    print(f"Cerrando {len(pids)} procesos anteriores...")
    for pid in pids:
        kill_process(pid)

    try:
        pid_file.unlink()
    except OSError:
        pass


def start_scripts(scripts):
    processes = []
    for script in scripts:
        print(f"Iniciando: {script}")
        proc = subprocess.Popen(
            [sys.executable, str(script)],
            cwd=str(script.parent),
            stdout=sys.stdout,
            stderr=sys.stderr,
            stdin=subprocess.DEVNULL,
        )
        processes.append(proc)
    return processes


def main():
    if not REPO_DIR.exists() or not REPO_DIR.is_dir():
        print(f"No se encontró la carpeta repo_clone en {REPO_DIR}")
        return

    scripts = find_python_scripts(REPO_DIR)
    if not scripts:
        print("No se encontraron scripts Python en repo_clone.")
        return

    kill_previous_processes(PID_FILE)

    processes = start_scripts(scripts)
    save_pids(PID_FILE, [proc.pid for proc in processes])

    print(f"Se iniciaron {len(processes)} procesos. PID guardados en {PID_FILE}.")


if __name__ == "__main__":
    main()
