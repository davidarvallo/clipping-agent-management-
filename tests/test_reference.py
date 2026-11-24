import tempfile
import unittest
from pathlib import Path
from scripts.analyze_reference import run

FAKE = '''
def download_video(url, work):
    (work/'video.mp4').write_bytes(b'fixture')
    return {'url':url}
def extract_keyframes(video, frames, fps):
    frames.mkdir()
    (frames/'frame.jpg').write_bytes(b'fixture')
def extract_audio(video, audio):
    audio.write_bytes(b'fixture')
def transcribe_with_whisper(audio, work, model):
    pass
'''

class ReferenceTests(unittest.TestCase):
    def test_distinct_urls_and_reruns_get_distinct_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root/'fake.py'; source.write_text(FAKE)
            urls = ['https://youtube.com/watch?v=one','https://youtube.com/watch?v=two','https://youtube.com/watch?v=one']
            outputs = [run(url, root/'out', source, skip_transcribe=True) for url in urls]
            self.assertEqual(len(set(outputs)), 3)
            for output in outputs:
                self.assertTrue((output/'manifest.json').exists())
                self.assertIn('awaiting review', (output/'summary.md').read_text())

    def test_missing_transcription_does_not_report_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root/'fake.py'; source.write_text(FAKE)
            with self.assertRaisesRegex(ValueError, 'transcription did not finish'):
                run('https://example.org/video', root/'out', source)

    def test_missing_frames_is_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root/'fake.py'
            source.write_text(FAKE.replace("(frames/'frame.jpg').write_bytes(b'fixture')", 'pass'))
            with self.assertRaisesRegex(ValueError, 'Frame extraction failed'):
                run('https://example.org/video', root/'out', source, skip_transcribe=True)
