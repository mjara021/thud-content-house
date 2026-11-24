# Thud's Archive — an AI agent content house

A [Claude Code](https://claude.com/claude-code) harness where a team of AI agents makes short
vertical history videos, start to finish, and posts them through the
[AiToEarn](https://aitoearn.ai) MCP server. The host of every video is **Thud**, a deadpan creature
made of stacked stones who has "seen it all" and is unimpressed by history's strangest
coincidences ("Woolly mammoths were still alive when the Great Pyramid was built." → *Noted.*).

The experiment: **how much of a content business can AI agents run by themselves?** Every run
writes an `AUTONOMY_REPORT.md` that scores each step as fully autonomous, needed a human, or failed.

![Thud's poses](tools/test/thud_poses.png)

## How it works

Type `/make-episode` in Claude Code inside this folder. The **Showrunner** (the main session)
runs the team, one step at a time:

| Step | Agent | Output |
|---|---|---|
| Series bible, topic ideas, script, hooks | `writer` | `SERIES_BIBLE.md`, `topics.md`, `script.md` |
| Topic pick, facts with 2+ sources, public-domain images | `researcher` | `research.md`, `assets/` + `assets.csv` |
| Fact, name, date and license check (can block) | `verifier` | `verification.md` |
| Exact build recipe | `strategist` | `build_spec.json` |
| Render, measure, look at frames, fix | `editor` | `final.mp4`, `cover.jpg` |
| 16-point checklist + quality score (can veto) | `watchdog` | `conformance.md`, `INTERVENTIONS.md` |
| Package, one yes/no from a human, post unlisted | Showrunner | `package.md`, `publish.md`, `AUTONOMY_REPORT.md` |

Agents live in `.claude/agents/`, their knowledge in `.claude/skills/` (`house-rules` is shared by
all of them; `make-episode` is the Showrunner's playbook). The full 32-specialist roadmap is in
[`ROSTER.md`](ROSTER.md).

## The video tools (free, local)

Python 3.9+ with Pillow, plus ffmpeg. See [`tools/README.md`](tools/README.md).

- `tools/thud.py` draws Thud identically every time.
- `tools/fetch_image.py` finds and downloads Wikimedia Commons / Library of Congress images and
  records each license (blocks share-alike, non-commercial and no-derivatives licenses).
- `tools/render.py` turns a `build_spec.json` into a 1080×1920 30fps MP4 with a pinned title card,
  word-by-word captions, pan/zoom over archival images, Thud's poses, a "Noted." stamp, a
  synthesized stone thud, and a loop ending.
- `tools/measure.py` checks length, size, codec, audio and cut rate, and makes a contact sheet and
  a safe-zone check image.

Try it: `python3 tools/render.py tools/test/assets_test/spec_real.json`

## House rules (short version)

$0 per video (no paid AI generation), every fact has 2+ independent sources, every image has a
recorded license, no franchise characters or real-person likeness, no fake engagement, and nothing
is posted without the Watchdog's approval and a human's yes.

## Notes

- The skills point to research files in the author's other folders (`content-research/`,
  `content-formula-research/`) that are not part of this repo, using absolute paths on the
  author's Mac. Change those paths if you run it elsewhere.
- Posting needs your own AiToEarn account connected to Claude Code (see `SETUP.md`). No keys are
  stored in this repo.
- Fonts: Anton and Archivo Black, SIL Open Font License (license files in `tools/fonts/`).
  Test image: Johann Jakob Frey, 1842, public domain, via Wikimedia Commons.
- No license has been chosen for the rest of this repo yet.
