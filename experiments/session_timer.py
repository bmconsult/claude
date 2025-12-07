"""
Session Timer - Track elapsed time in autonomous sessions

Usage:
    python session_timer.py start    # Start tracking
    python session_timer.py check    # Check elapsed time
    python session_timer.py          # Same as check
"""

import sys
import time
import json
from pathlib import Path

TIMER_FILE = Path("/home/user/claude/experiments/.session_timer")


def start():
    """Start a new timer."""
    data = {
        "start_time": time.time(),
        "start_iso": time.strftime("%Y-%m-%d %H:%M:%S"),
        "markers": []
    }
    TIMER_FILE.write_text(json.dumps(data, indent=2))
    print(f"Timer started at {data['start_iso']}")


def check():
    """Check elapsed time."""
    if not TIMER_FILE.exists():
        print("No timer running. Use 'python session_timer.py start' to begin.")
        return

    data = json.loads(TIMER_FILE.read_text())
    elapsed = time.time() - data["start_time"]

    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)

    if hours > 0:
        print(f"Elapsed: {hours}h {minutes}m {seconds}s")
    elif minutes > 0:
        print(f"Elapsed: {minutes}m {seconds}s")
    else:
        print(f"Elapsed: {seconds}s")

    print(f"Started: {data['start_iso']}")
    print(f"Now: {time.strftime('%Y-%m-%d %H:%M:%S')}")


def mark(label="checkpoint"):
    """Add a marker to track session phases."""
    if not TIMER_FILE.exists():
        print("No timer running.")
        return

    data = json.loads(TIMER_FILE.read_text())
    elapsed = time.time() - data["start_time"]
    data["markers"].append({
        "label": label,
        "elapsed_seconds": elapsed,
        "time_iso": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    TIMER_FILE.write_text(json.dumps(data, indent=2))
    print(f"Marked '{label}' at {elapsed/60:.1f} minutes")


def main():
    if len(sys.argv) < 2:
        check()
    elif sys.argv[1] == "start":
        start()
    elif sys.argv[1] == "check":
        check()
    elif sys.argv[1] == "mark":
        label = sys.argv[2] if len(sys.argv) > 2 else "checkpoint"
        mark(label)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
