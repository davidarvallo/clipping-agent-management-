import contextlib
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import toolkit


class ToolkitTests(unittest.TestCase):
    def test_catalog_has_unique_pinned_sources(self):
        import json
        rows = json.loads((toolkit.ROOT / 'integrations/toolkit.json').read_text())
        self.assertEqual(len(rows), len(toolkit.catalog()))
        for row in rows:
            self.assertRegex(row['revision'], r'^[0-9a-f]{40}$')
            self.assertRegex(row['repo'], r'^[\w.-]+/[\w.-]+$')

    def test_unknown_source_cannot_escape_directory(self):
        with self.assertRaises(ValueError):
            toolkit.fetch_source('../elsewhere')

    def test_existing_source_is_preserved(self):
        with tempfile.TemporaryDirectory() as d, patch.object(toolkit, 'SOURCES', Path(d)):
            p = Path(d) / 'gsap-skills'
            p.mkdir()
            (p / 'mine').write_text('keep')
            with self.assertRaises(ValueError):
                toolkit.fetch_source('gsap-skills')
            self.assertEqual((p / 'mine').read_text(), 'keep')

    def test_fetch_pin_and_failure_cleanup(self):
        pin = toolkit.catalog()['gsap-skills']['revision']
        with tempfile.TemporaryDirectory() as d, patch.object(toolkit, 'SOURCES', Path(d)), patch('toolkit.shutil.which', return_value='/bin/git'), patch('toolkit.subprocess.run') as run, patch('toolkit.subprocess.check_output', return_value=pin+'\n'):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(toolkit.fetch_source('gsap-skills'), 0)
            self.assertIn(pin, run.call_args_list[1].args[0])
        with tempfile.TemporaryDirectory() as d, patch.object(toolkit, 'SOURCES', Path(d)), patch('toolkit.shutil.which', return_value='/bin/git'), patch('toolkit.subprocess.run', side_effect=OSError('offline')):
            with self.assertRaises(OSError):
                toolkit.fetch_source('gsap-skills')
            self.assertFalse((Path(d)/'gsap-skills').exists())

    def test_native_args_and_exit_status(self):
        with patch('toolkit.shutil.which', return_value='/bin/ffmpeg'), patch('toolkit.subprocess.call', return_value=7) as call:
            self.assertEqual(toolkit.main('ffmpeg', ['-i', 'file with spaces.mp4']), 7)
            call.assert_called_once_with(['/bin/ffmpeg', '-i', 'file with spaces.mp4'])

    def test_missing_dependency(self):
        with patch('toolkit.shutil.which', return_value=None), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(toolkit.main('manim', ['--version']), 2)

    def test_existing_command_help(self):
        import clipping
        for command in clipping.COMMANDS:
            result = subprocess.run(['python3', str(toolkit.ROOT/'clipping.py'), command, '--help'], capture_output=True)
            direct = subprocess.run(['python3', str(toolkit.ROOT/clipping.COMMANDS[command]), '--help'], capture_output=True)
            self.assertEqual(result.returncode, direct.returncode, command)
            self.assertEqual(result.stdout, direct.stdout, command)
            self.assertEqual(result.stderr, direct.stderr, command)

if __name__ == '__main__':
    unittest.main()
