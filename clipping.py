#!/usr/bin/env python3
"""One entry point for the independently maintained content tools."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMANDS = {
    "instagram-research": "integrations/instagram/skills/ig-viral/swipe.py",
    "youtube-research": "integrations/youtube/skills/yt-viral/swipe.py",
    "reel-beats": "integrations/instagram/skills/ig-reel/beats.py",
    "reel-hooks": "integrations/instagram/skills/ig-reel/hookscore.py",
    "youtube-hooks": "integrations/youtube/skills/yt-script/hookscore.py",
}

def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python3 clipping.py COMMAND [tool arguments]")
        print("Commands: " + ", ".join(COMMANDS))
        return 0 if len(sys.argv) > 1 else 2
    command = sys.argv[1]
    if command not in COMMANDS:
        print(f"Unknown command: {command}", file=sys.stderr)
        return 2
    return subprocess.call([sys.executable, str(ROOT / COMMANDS[command]), *sys.argv[2:]])

if __name__ == "__main__":
    raise SystemExit(main())
