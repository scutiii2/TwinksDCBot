from __future__ import annotations
import sys
from pathlib import Path
from filelock import FileLock, Timeout

LOCK_FILE = Path("storage/twinks.lock")

_lock: FileLock | None = None


def acquire() -> None:
    """Prevent a second instance of the bot from starting.

    Uses an OS-level advisory lock rather than a PID-in-a-file check: the
    kernel releases it automatically the instant this process exits, for
    any reason (crash, SIGKILL, container restart). A PID check doesn't
    survive a container restart - PID namespaces reset, so a stale PID
    left behind by an unclean shutdown will almost always collide with
    some real process (often PID 1) in the new container, wrongly
    reporting the bot as already running.
    """
    global _lock
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)

    _lock = FileLock(str(LOCK_FILE), timeout=0)
    try:
        _lock.acquire()
    except Timeout:
        print(
            "Another instance of Twinks is already running. "
            "Kill it before starting a new one."
        )
        sys.exit(1)


def release() -> None:
    global _lock
    if _lock is not None:
        _lock.release()
        _lock = None
