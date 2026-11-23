#!/usr/bin/env python3
"""One entry point for the independently maintained content tools."""
import subprocess
import sys
import shutil
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parent
COMMANDS = {
    "instagram-research": "integrations/instagram/skills/ig-viral/swipe.py",
    "youtube-research": "integrations/youtube/skills/yt-viral/swipe.py",
    "reel-beats": "integrations/instagram/skills/ig-reel/beats.py",
    "reel-hooks": "integrations/instagram/skills/ig-reel/hookscore.py",
    "youtube-hooks": "integrations/youtube/skills/yt-script/hookscore.py",
}

OPTIONAL = {
    "hyperframes": "npm install --save-dev hyperframes (requires Node.js 22+ and FFmpeg)",
    "auto-editor": "Install Auto-Editor: https://auto-editor.com/installing",
    "pascal": "Install @pascal-app/cli: https://github.com/pascalorg/editor",
}

def binary(name: str) -> Optional[str]:
    if name == "hyperframes":
        local = ROOT / "node_modules" / ".bin" / "hyperframes"
        if local.is_file():
            return str(local)
    return shutil.which(name)

def optional_tool(command: str, args: List[str]) -> int:
    if command == "video-status":
        for name, install in OPTIONAL.items():
            found = binary(name)
            print(f"{name}: {found or 'not installed'}")
            if not found:
                print(f"  {install}")
        return 0
    name = "hyperframes" if command.startswith("video-") else "auto-editor" if command == "trim" else "pascal"
    executable = binary(name)
    if not executable:
        print(f"{name} is not installed. {OPTIONAL[name]}", file=sys.stderr)
        return 2
    if command == "video-init":
        if len(args) != 1:
            print("Usage: video-init PROJECT_NAME", file=sys.stderr)
            return 2
        argv, cwd = [executable, "init", args[0]], None
    elif command in ("video-preview", "video-render"):
        if len(args) != 1 or not Path(args[0]).is_dir():
            print(f"Usage: {command} EXISTING_PROJECT_DIRECTORY", file=sys.stderr)
            return 2
        argv, cwd = [executable, command[len("video-"):]], args[0]
    elif command == "trim":
        if not args or not Path(args[0]).is_file():
            print("Usage: trim EXISTING_VIDEO [auto-editor options]", file=sys.stderr)
            return 2
        argv, cwd = [executable, *args], None
    else:
        argv, cwd = [executable, "editor"], None
    try:
        return subprocess.call(argv, cwd=cwd)
    except OSError as exc:
        print(f"Could not start {name}: {exc}", file=sys.stderr)
        return 1

def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python3 clipping.py COMMAND [tool arguments]")
        print("Commands: " + ", ".join(COMMANDS))
        print("Optional: video-status, video-init, video-preview, video-render, trim, pascal-editor")
        return 0 if len(sys.argv) > 1 else 2
    command = sys.argv[1]
    if command in ("video-status", "video-init", "video-preview", "video-render", "trim", "pascal-editor"):
        return optional_tool(command, sys.argv[2:])
    if command not in COMMANDS:
        print(f"Unknown command: {command}", file=sys.stderr)
        return 2
    return subprocess.call([sys.executable, str(ROOT / COMMANDS[command]), *sys.argv[2:]])

if __name__ == "__main__":
    raise SystemExit(main())
