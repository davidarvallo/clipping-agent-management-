# Optional production toolkit

HyperFrames remains the primary assembly/rendering path. Existing Instagram and YouTube tools remain independent. The catalog pins optional repositories to reviewed source revisions; fetching preserves their source and license files in `external/`. Sources are downloaded only on request and are not bundled into this repository. Fetching does not install packages, register agent skills, connect MCP, render, or publish.

## Start here

```bash
python3 clipping.py video-status
python3 clipping.py toolkit-list
python3 clipping.py toolkit-fetch gsap-skills
python3 clipping.py ffmpeg -version
python3 clipping.py ffprobe -v error -show_format -show_streams -of json episode.mp4
```

Install FFmpeg from https://ffmpeg.org/download.html and HyperFrames following the main README. Use GSAP instructions from the fetched repository when authoring animations; install the `gsap` package in the actual video project. Animations must follow HyperFrames' seekable timeline requirements. A source checkout alone does not enable an agent capability.

## Select tools by episode

| Catalog ID | Use | Integration boundary |
| --- | --- | --- |
| gsap-skills | Text, transitions, timed movement | Guidance; requires GSAP in the video project |
| blender-mcp | General 3D scenes and models | Requires Blender, addon, MCP client/server configuration |
| shotcraft | Product and website promos | Separate Remotion project; rendered footage can enter HyperFrames |
| remotion-skills | Remotion captions, compositions and rendering guidance | Use alongside Shotcraft; not a replacement for installed Remotion |
| manim | Mathematical/educational diagrams | Separate Python environment; render media and import it |
| three | Browser 3D | Add to the specific project and control rendering by frame/time |
| react-three-fiber | React-based 3D | Only for React projects such as Remotion |
| matter | 2D collisions and simulations | Precompute or deterministically step simulations for video |
| rapier | 2D/3D physics | Alternative physics engine; select per project |
| particles | Particle effects | Seed randomness and control time for repeatable rendering |
| p5 | Generative visuals | Render deterministic frames or export a clip |
| lottie | Existing exported animations | Control animation by frame; verify exported asset compatibility |

Fetch one with `python3 clipping.py toolkit-fetch TOOL_ID`. Existing directories are never overwritten. If a download fails, only the new incomplete directory is removed. Updating a pin is an explicit catalog edit followed by validation. Source presence is not an installation or health check.

## Native tool adapters

```bash
python3 clipping.py ffmpeg -n -i input.mp4 -c:v libx264 -crf 20 -c:a aac output.mp4
python3 clipping.py blender --background scene.blend --render-anim
python3 clipping.py manim -ql scene.py MyScene
```

These pass arguments directly to installed executables without a shell. Native flags retain their normal behavior, including overwrite behavior. Use `-n` for FFmpeg when existing outputs should be preserved. Install Blender from https://www.blender.org/download/ and Manim using https://docs.manim.community/en/stable/installation.html in a separate environment.

For Blender MCP, follow the pinned source README to install its addon and configure a compatible local MCP client. Blender must be running for its MCP connection. The adapter does not auto-connect this ChatGPT session. Render assets to files and import those files into the main episode.

For Shotcraft, follow its pinned README and install matching Remotion dependencies in a separate project. Check Remotion's current licensing for your use before commercial deployment. The Shotcraft source license does not cover all dependencies or input assets. Preserve upstream licenses when distributing source.

## Deliberately deferred

Anime.js, Motion and Theatre.js overlap with the chosen animation path. Motion Canvas adds another production engine. Impeccable is dashboard design guidance; the general Anthropic skills collection should be selected from when a specific capability is needed. None are required for today's clipping workflow.

## Validation boundaries

Run `python3 -m unittest discover -s tests -v`. Tests cover routing, dependency errors, pinned fetch behavior and existing command entry points. Passing these tests does not certify Blender MCP connectivity, optional package compatibility, actual video renders, social account access or viral performance. Run a real representative render after installing each production tool.
