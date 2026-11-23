# Clipping Agent Management

One workspace for researching repeatable short-video ideas, drafting episodes, producing visuals, and reviewing results. The content can cover any subject; the survival Reel is one example of a repeatable format.

## How the pieces fit

1. **Discover:** Gather public Reels and YouTube Shorts in a topic. Capture several recent videos per account/channel and their view counts. The research tools compare an individual video's views with that creator's usual views. They do not fetch social-media data automatically.
2. **Select:** Compare standout hooks, visual payoffs, and comments. Write an original premise with enough variation for multiple episodes.
3. **Script:** Use the Instagram or YouTube skill instructions in `integrations/` to draft the hook, voiceover, scene list, and end question. Choose a format based on the destination platform.
4. **Produce:** Generate or collect visuals, then assemble and render the vertical video with HyperFrames. Higgsfield or Artlist can provide source footage when connected; this repository does not require either service.
5. **Publish and learn:** Publish manually at first. The [Blotato publishing guide](https://github.com/cporter202/automate-faceless-content) describes scheduling, cross-posting, and comment-to-DM workflows if those become useful. Record the post's results and audience questions before writing the next episode.

## Quick commands

Python 3 runs the included local tools; no account credentials are needed to process data you provide.

```bash
python3 clipping.py --help
python3 clipping.py instagram-research collected-reels.tsv --out ideas.md
python3 clipping.py youtube-research collected-shorts.json --min 2.0
python3 clipping.py reel-beats script.txt --target 30
python3 clipping.py reel-hooks hooks.txt
python3 clipping.py video-status
```

Instagram TSV header: `account\tfollowers\tmedian\tviews\thook`. The median is that account's recent typical Reel views. YouTube JSON is an array of objects with `channel`, `title`, `views`, `url`, and `duration`; include at least four videos per channel. See `integrations/instagram/skills/ig-viral/SKILL.md` and `integrations/youtube/skills/yt-viral/SKILL.md` for collection details. The tools analyze provided data; they cannot certify that a format will go viral.

## Video production (optional tools)

These are external tools invoked only by the command you choose. They are not bundled into this repository, and no downloads, services, AI credits, or publishing happen when running research commands. Run `python3 clipping.py video-status` to see what is installed.

**HyperFrames** is the main assembly and rendering option. It requires Node.js 22+ and FFmpeg. Install it in this repo with `npm install --save-dev hyperframes`, then:

```bash
python3 clipping.py video-init my-episode
python3 clipping.py video-preview my-episode
python3 clipping.py video-render my-episode
```

HyperFrames projects contain editable HTML/CSS/JS and media. Preview the episode before rendering; its own [documentation](https://github.com/heygen-com/hyperframes) describes the project format. Local rendering does not by itself create AI footage or publish anything.

**Auto-Editor** is an optional first pass on footage with silence or inactive sections. [Install it separately](https://auto-editor.com/installing), then run `python3 clipping.py trim footage.mp4`. Review the cuts before using that output as a HyperFrames input. For illustrated videos that do not start from a recording, skip it.

**Pascal Editor** is an optional architecture source for videos about buildings, rooms, or construction. [Install its CLI](https://github.com/pascalorg/editor), then `python3 clipping.py pascal-editor` opens its local building editor. Export or record the visuals you want, and import that media into HyperFrames. There is no automatic conversion of a Pascal scene into a finished video.

## Sources and boundaries

- `integrations/instagram/`: [Instagram agent skill](https://github.com/Jakeschincariol/instagram-agent-skill), copied with its MIT license.
- `integrations/youtube/`: [YouTube agent skill](https://github.com/Jakeschincariol/youtube-agent-skill), copied with its MIT license.
- [Automate faceless content](https://github.com/cporter202/automate-faceless-content): linked as an external publishing guide. Its README discloses Blotato sponsorship; no license was listed when this project was assembled, so its files were not copied.
- [HyperFrames](https://github.com/heygen-com/hyperframes), [Auto-Editor](https://github.com/WyattBlue/auto-editor), and [Pascal Editor](https://github.com/pascalorg/editor): optional external programs. Their source code is not copied into this repo.

The original repositories remain independent. These folders are separate to avoid filename and command collisions. Nothing in this repository connects to Instagram, YouTube, Higgsfield, or Blotato automatically or publishes a post without a separate setup.

## Production toolkit

The [optional toolkit](docs/production-toolkit.md) adds pinned source fetching for GSAP guidance, Blender MCP, Shotcraft/Remotion guidance, Manim, Three.js, React Three Fiber, Matter.js, Rapier, tsParticles, p5.js and Lottie. These are selected per project; they do not load into research commands.

```bash
python3 clipping.py toolkit-list
python3 clipping.py toolkit-fetch gsap-skills
python3 clipping.py ffmpeg -version
python3 clipping.py ffprobe -v error -show_streams -of json episode.mp4
python3 -m unittest discover -s tests -v
```

`ffmpeg`, `ffprobe`, `blender` and `manim` commands invoke separately installed programs. The source catalog is in `integrations/toolkit.json`. Downloading source does not install dependencies, activate skills or connect accounts. See the toolkit guide for project-specific setup and validation boundaries.
