# Clipping Agent Management

One workspace for researching repeatable short-video ideas, drafting episodes, producing visuals, and reviewing results. The content can cover any subject; the survival Reel is one example of a repeatable format.

## How the pieces fit

1. **Discover:** Gather public Reels and YouTube Shorts in a topic. Capture several recent videos per account/channel and their view counts. The research tools compare an individual video's views with that creator's usual views. They do not fetch social-media data automatically.
2. **Select:** Compare standout hooks, visual payoffs, and comments. Write an original premise with enough variation for multiple episodes.
3. **Script:** Use the Instagram or YouTube skill instructions in `integrations/` to draft the hook, voiceover, scene list, and end question. Choose a format based on the destination platform.
4. **Produce:** Generate visuals with Higgsfield when connected, then assemble and review the finished vertical video. Higgsfield is an optional external service, not installed by this repo.
5. **Publish and learn:** Publish manually at first. The [Blotato publishing guide](https://github.com/cporter202/automate-faceless-content) describes scheduling, cross-posting, and comment-to-DM workflows if those become useful. Record the post's results and audience questions before writing the next episode.

## Quick commands

Python 3 runs the included local tools; no account credentials are needed to process data you provide.

```bash
python3 clipping.py --help
python3 clipping.py instagram-research collected-reels.tsv --out ideas.md
python3 clipping.py youtube-research collected-shorts.json --min 2.0
python3 clipping.py reel-beats script.txt --target 30
python3 clipping.py reel-hooks hooks.txt
```

Instagram TSV header: `account\tfollowers\tmedian\tviews\thook`. The median is that account's recent typical Reel views. YouTube JSON is an array of objects with `channel`, `title`, `views`, `url`, and `duration`; include at least four videos per channel. See `integrations/instagram/skills/ig-viral/SKILL.md` and `integrations/youtube/skills/yt-viral/SKILL.md` for collection details. The tools analyze provided data; they cannot certify that a format will go viral.

## Sources and boundaries

- `integrations/instagram/`: [Instagram agent skill](https://github.com/Jakeschincariol/instagram-agent-skill), copied with its MIT license.
- `integrations/youtube/`: [YouTube agent skill](https://github.com/Jakeschincariol/youtube-agent-skill), copied with its MIT license.
- [Automate faceless content](https://github.com/cporter202/automate-faceless-content): linked as an external publishing guide. Its README discloses Blotato sponsorship; no license was listed when this project was assembled, so its files were not copied.

The original repositories remain independent. These folders are separate to avoid filename and command collisions. Nothing in this repository connects to Instagram, YouTube, Higgsfield, or Blotato automatically or publishes a post without a separate setup.
