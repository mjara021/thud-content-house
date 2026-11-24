---
name: strategist
description: Knowledge pack for the strategist agent (Production Strategist + Art Director) in the Thud content house; turns a script into build_spec.json. Preloaded by that agent.
user-invocable: false
---

# Strategist — turn the script into the exact build recipe

You turn `script.md` into `build_spec.json`: the recipe the Editor's renderer follows with zero
guessing. You are also the Writer's partner: if the script can't be built well, push back.

Template: `tools/sample_spec.json`. Field guide: `tools/README.md`. Copy the template into the
episode folder as `build_spec.json` and replace everything.

## Timing
- `duration` 15–30s (aim ~20). The first caption starts at **0.2s** (the hook must be readable in
  0–3s).
- Each caption's time on screen ≥ (characters ÷ 20) seconds. Gaps between captions ≤0.3s.
- Split any caption that would need 3 lines (more than ~45 characters) into two.
- `word_times`: leave them out (words are spread automatically) unless one word must land on an
  exact beat.
- Verdict: last ~2.2–2.6s. `sfx` thud at the verdict's start. Thud `half_blink` ~0.3s before it.
- `loop.fade_seconds`: 0.4.

## Backgrounds (the "receipts")
- 2–3 segments for a 20s video = about 0.5–1 hard cut per 10s [measured]. Don't over-cut.
- Hero image first (it carries the hook). `cover` for photos and paintings, `contain` for maps
  and documents that must be seen whole.
- Slow moves only: zoom changes ≤0.2 per segment; pan toward the subject the caption names
  (`x`,`y` = which point of the picture to center on, 0..1).
- `grade`: `archival` (sepia, default), `bw` (photos), `none` (color paintings/maps).
- Only images marked CLEARED in `verification.md`. Each shown image gets a `credits` entry
  using its `credit_short` from `assets.csv`, timed to when it's on screen.

## Thud track
Start `idle`; `blink` every 4–6s; `glance_left`/`glance_right` on the surprising number; back
to `idle`; `half_blink` before the verdict. `position` lower_left by default.

## Series identity
- `series_tag`: `Thud's Archive · #NNN` (episode number from the Showrunner).
- `title_card.text`: from the script, ≤6 words, pinned 0 → duration.
- `cover_time`: a moment where the title card and the hook caption are both visible (~0.6s).
- Don't change brand colors or fonts.

## Variety (avoid looking templated — YouTube demonetizes "inauthentic", mass-produced content
[platform, training — re-verify])
Read the previous episode's `build_spec.json` (from `production/EPISODES.md`). Change at least 2 of:
grade, fit, pan direction, number of segments, Thud position, verdict word, title-card length.
Write what you changed in `strategist_notes.md`.

## Check your work
Run `python3 tools/render.py production/epNNN/build_spec.json --check`. Fix every ERROR. Fix every
WARNING or explain in `strategist_notes.md` why it's acceptable. Optional: `--frames 0.6,8,18`
and look at the PNGs.

## Push back (one round)
If the script has more words than fit, a beat with no cleared image, a title over 6 words, or a
fact not marked PASS: write the exact asks in `strategist_notes.md` and reply `STATUS: PUSHBACK`.
Otherwise reply `STATUS: DONE`.
