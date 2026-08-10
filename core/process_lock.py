from __future__ import annotations
import os
import sys
from pathlib import Path

LOCK_FILE = Path("storage/twinks.lock")


def acquire() -> None:
    """Prevent a second instance of the bot from starting.

    Writes the current PID to a lock file. If a lock file already exists
    and that PID is still alive, refuses to start.
    """
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)

    if LOCK_FILE.exists():
        old_pid = LOCK_FILE.read_text().strip()
        if old_pid.isdigit() and _pid_alive(int(old_pid)):
            print(
                f"Another instance of Twinks is already running (PID {old_pid}). "
                f"Kill it before starting a new one."
            )
            sys.exit(1)

    LOCK_FILE.write_text(str(os.getpid()))


def release() -> None:
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True