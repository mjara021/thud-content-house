---
name: editor
description: Knowledge pack for the editor agent (Motion Editor & Sound Designer) in the Thud content house; renders and self-checks the video. Preloaded by that agent.
user-invocable: false
---

# Editor — render it, look at it, fix it

## Render and measure
```
python3 tools/render.py production/epNNN/build_spec.json
python3 tools/measure.py production/epNNN/final.mp4
python3 tools/render.py production/epNNN/build_spec.json --frames 0.6,<mid>,<verdict+0.3>,<duration-0.1>
```
Rendering takes about 40 seconds. `measure.json` must say `"all_pass": true`.

## Look at the pictures (use Read on each image file)
`contact_sheet.jpg` (one frame per second), `safezone_check.jpg`, `cover.jpg`, and the preview
PNGs. Check:
- Every caption is readable and inside the safe area (not in the red zones).
- Captions, Thud and the credit never overlap each other.
- The image on screen matches what the caption is talking about.
- No awkward crops (cut-off heads, text in the image chopped mid-word) and nothing blurry.
- The cover works as a thumbnail: title card + hook caption visible, image readable.
- The verdict stamp lands, Thud is half-blinking, and the last frame looks like the first (loop).
- `render_report.json` has no warnings you can fix.

## What you may change (in `build_spec.json`)
Timing nudges, caption splits (same words), `move`/`x`/`y`/`zoom` framing, `fit`, `grade`,
Thud poses and position, `cover_time`. **Max 3 render rounds.**

## What you may not change
Words, facts, title or verdict (send to the Writer), images (send to the Researcher), the tools'
code or Thud's look (write it under "Tool problems" so the founders can fix it later).

## Sound [practitioner, training]
- The renderer adds a silent stereo track plus our own synthesized thud at each `sfx` time. Some
  apps handle videos with no audio track badly, so the silent track stays.
- Music only if the spec has a public-domain recording or CC0 file with its license. A
  public-domain *composition* (e.g. Beethoven) is not the same as a public-domain *recording*.
- If music is used: around −14 LUFS integrated, true peak ≤ −1 dBFS.

## Export spec (the renderer does this; check `measure.json`)
1080×1920, 30 fps, H.264 high profile, yuv420p, AAC 48 kHz, fast-start, 15–30s.

## Output — `editor_notes.md`
Rounds rendered, what you changed and why, what you checked and saw, anything you couldn't fix
(and who should), and "Tool problems" if any. Reply in the ≤150-word house format.
