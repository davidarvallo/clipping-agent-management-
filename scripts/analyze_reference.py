#!/usr/bin/env python3
"""Run the pinned reference analyzer in a unique directory and verify outputs."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(url, output_root, source, fps=1.0, model='base', skip_transcribe=False):
    if not source.is_file():
        raise ValueError('Fetch source first: python3 clipping.py toolkit-fetch video-analyzer')
    if not url.startswith(('https://', 'http://')):
        raise ValueError('Provide an HTTP(S) video URL.')
    if not 0 < fps <= 10:
        raise ValueError('fps must be greater than zero and at most 10.')
    spec = importlib.util.spec_from_file_location('reference_upstream', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    output_root.mkdir(parents=True, exist_ok=True)
    # Unique per execution: different watch?v= links and reruns cannot mix files.
    work = Path(tempfile.mkdtemp(prefix='reference-', dir=output_root))
    print(f'Output directory: {work}', flush=True)
    info = module.download_video(url, work)
    videos = [p for p in work.glob('video.*') if p.suffix in ('.mp4', '.mkv', '.webm', '.mov') and p.stat().st_size]
    if len(videos) != 1:
        raise ValueError(f'Expected one downloaded video in {work}')
    module.extract_keyframes(videos[0], work / 'frames', fps=fps)
    if not any(p.stat().st_size for p in (work / 'frames').glob('*.jpg')):
        raise ValueError(f'Frame extraction failed: {work}')
    if not skip_transcribe:
        audio = work / 'audio.wav'
        module.extract_audio(videos[0], audio)
        if not audio.exists() or not audio.stat().st_size:
            raise ValueError(f'Audio extraction failed: {work}')
        module.transcribe_with_whisper(audio, work, model=model)
        for name in ('transcript.txt', 'transcript.srt'):
            if not (work / name).is_file():
                raise ValueError(f'Missing {name}; transcription did not finish: {work}')
    (work / 'summary.md').write_text('# Reference analysis\n\nStatus: awaiting review.\n\nReview hook, visual style, pacing, story beats and original variations.\nTreat explanations of performance as hypotheses, not proven causes.\n', encoding='utf-8')
    (work / 'manifest.json').write_text(json.dumps({'source_url': url, 'metadata': info, 'transcription_requested': not skip_transcribe, 'analysis_status': 'awaiting_review'}, indent=2), encoding='utf-8')
    return work


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url')
    parser.add_argument('--output-root', type=Path, default=ROOT/'runs'/'analysis')
    parser.add_argument('--fps', type=float, default=1.0)
    parser.add_argument('--whisper-model', default='base', choices=['tiny','base','small','medium','large','turbo'])
    parser.add_argument('--skip-transcribe', action='store_true')
    args = parser.parse_args()
    try:
        work = run(args.url, args.output_root, ROOT/'external'/'video-analyzer'/'analyze_viral_video.py', args.fps, args.whisper_model, args.skip_transcribe)
        print(f'Assets verified: {work}. Content analysis still requires review.')
        return 0
    except (ValueError, OSError, ImportError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
