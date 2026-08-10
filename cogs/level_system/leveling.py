from __future__ import annotations


def _xp_needed(level: int) -> int:
    """XP required to advance from `level` to `level + 1`."""
    return 5 * level * level + 50 * level + 100


def level_from_xp(total_xp: int) -> int:
    """Derive a user's current level from their lifetime total XP."""
    level = 0
    remaining = total_xp
    while remaining >= _xp_needed(level):
        remaining -= _xp_needed(level)
        level += 1
    return level


def xp_for_level(level: int) -> int:
    """Total lifetime XP required to reach `level`."""
    return sum(_xp_needed(n) for n in range(level))


def xp_progress(total_xp: int) -> tuple[int, int, int]:
    """Return (level, xp_into_current_level, xp_needed_for_next_level)."""
    level = level_from_xp(total_xp)
    into_level = total_xp - xp_for_level(level)
    return level, into_level, _xp_needed(level)