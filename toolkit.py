"""Optional production tools. No dependencies beyond Python's standard library."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / 'external'


def catalog():
    return {item['id']: item for item in json.loads((ROOT / 'integrations/toolkit.json').read_text())}


def fetch_source(name):
    items = catalog()
    if name not in items:
        raise ValueError('Unknown tool. Run toolkit-list for supported names.')
    item = items[name]
    target = SOURCES / name
    if target.exists():
        raise ValueError(f'{target} already exists; leaving it untouched.')
    if not shutil.which('git'):
        raise ValueError('Install Git before fetching optional sources.')
    SOURCES.mkdir(exist_ok=True)
    target.mkdir()
    try:
        subprocess.run(['git', 'init', str(target)], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(target), 'fetch', '--depth=1',
                        'https://github.com/' + item['repo'] + '.git', item['revision']], check=True)
        subprocess.run(['git', '-C', str(target), 'checkout', '--detach', 'FETCH_HEAD'], check=True)
        actual = subprocess.check_output(['git', '-C', str(target), 'rev-parse', 'HEAD'], text=True).strip()
        if actual != item['revision']:
            raise ValueError('Fetched revision does not match the pinned source.')
    except Exception:
        shutil.rmtree(target)
        raise
    print(f'Source ready: {target}\nRead its README for dependencies and setup. Nothing was installed or connected.')
    return 0


def main(command, args):
    try:
        if command == 'toolkit-list':
            for name, item in catalog().items():
                state = 'source present' if (SOURCES / name).exists() else 'not fetched'
                print(f"{name}: {item['purpose']} [{state}]")
            return 0
        if command == 'toolkit-fetch':
            if len(args) != 1:
                raise ValueError('Usage: toolkit-fetch TOOL_NAME')
            return fetch_source(args[0])
        executable = shutil.which(command)
        if not executable:
            raise ValueError(f'{command} is not installed. See docs/production-toolkit.md.')
        if not args:
            raise ValueError(f'Usage: {command} [native tool arguments]')
        return subprocess.call([executable, *args])
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
