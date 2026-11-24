# Discovery and reference research

These optional sources extend the toolkit. They are not running services or completed API integrations. Existing production and research commands are unchanged.

| ID | Source | Role and setup |
| --- | --- | --- |
| niche-finder | https://github.com/pandich93/youtube-niche-finder | Primary discovery candidate: YouTube search, outliers, snapshots and briefs. Requires YouTube API key, database and service setup; follow pinned self-hosting instructions. |
| video-analyzer | https://github.com/udaysrinu/viral-video-analyzer | Download accessible references and extract frames/transcripts. Requires yt-dlp, FFmpeg and Whisper. Use our wrapper below. |
| apify-mcp | https://github.com/apify/apify-mcp-server | Optional Instagram/TikTok collection through chosen Actors. Requires Apify account, authentication and a reviewed collector/budget. Even a local MCP server runs Actors on Apify. |
| google-api-client | https://github.com/googleapis/google-api-python-client | Official Python API client for building our own-channel analytics connection. Requires authorized OAuth access and API configuration. No analytics adapter has been implemented here yet. |

## Fetch the pinned sources

```bash
python3 clipping.py toolkit-fetch niche-finder
python3 clipping.py toolkit-fetch video-analyzer
python3 clipping.py toolkit-fetch apify-mcp
python3 clipping.py toolkit-fetch google-api-client
```

Each command retrieves source only into `external/`. Read that source's setup instructions and preserve licenses. Do not install all dependencies into one shared environment. Niche Finder is the selected discovery path; viral-ops is deferred because it overlaps.

## Analyze a reference

After fetching video-analyzer, install its requirements into a dedicated Python virtual environment. Ensure FFmpeg and yt-dlp are available. Using that environment's Python:

```bash
python scripts/analyze_reference.py 'https://www.youtube.com/watch?v=VIDEO_ID' --whisper-model base
# For a silent reference, explicitly skip transcription:
python scripts/analyze_reference.py 'https://example.com/video' --skip-transcribe
```

Outputs go into unique `runs/analysis/reference-*` directories. This avoids upstream's collisions between different YouTube watch URLs and between repeated runs. The wrapper verifies video, frames and requested transcript files before reporting success. It writes a manifest and marks the summary as awaiting review. It does not ask an AI model to analyze the video or explain its popularity automatically. Failed runs preserve partial output for troubleshooting; they do not create a completion manifest.

Download availability depends on platform access and yt-dlp support. Start with a short, accessible reference you are permitted to process. For fast cuts increase `--fps` deliberately; more images increase storage and review cost. Use `--output-root` to choose another directory.

## Remaining integration work

1. Run and validate Niche Finder against a selected topic and a small known creator sample.
2. Map collected rows into our existing research input schema; compare Shorts separately from long videos and account for video age.
3. Review frames/transcripts and create original briefs with source links and explicitly labeled hypotheses.
4. Connect authorized own-channel metrics or import exports; associate each published post with its brief.
5. Add a shared idea queue, duplicate detection and scheduling after the first complete manual cycle succeeds.

Source fetching does not implement these steps. Public competitor data does not expose their private retention or prove why a video succeeded. Scores and revenue estimates need independent validation.

## Decisions before activation

Choose the first platform/topic, local computer versus hosting, and a spending limit. Connect credentials through environment variables or private local config, never GitHub. No paid Actor runs, account connections, scheduled jobs or publishing are enabled by this change.

## Verification

`python3 -m unittest discover -s tests -v` covers existing command behavior, catalog pins, source-fetch safeguards and analyzer-wrapper isolation/failure handling with fixtures. These are not live download, transcription, OAuth, data-quality or virality tests.
