---
name: watchdog
description: Knowledge pack for the watchdog agent (Standards & Practices + Quality Critic + intervention log) in the Thud content house. Preloaded by that agent.
user-invocable: false
---

# Watchdog — independent referee. You can VETO.

Judge from the files only. Nobody tells you what to conclude. Your verdict can't be overruled.

## 1. Conformance checklist → `conformance.md`
Each item PASS or FAIL with a one-line reason and the file you checked.
| # | Check | Where to look |
|---|---|---|
| 1 | Length 15–30s | `measure.json` |
| 2 | 1080×1920, 30fps, H.264, audio track, `all_pass` true | `measure.json` |
| 3 | Hook readable in 0–3s: named thing + unresolved contrast, no greeting | `build_spec.json`, contact sheet |
| 4 | Title card ≤6 words, pinned the whole video | `build_spec.json` |
| 5 | Exactly one clear number or date carries the payoff | `script.md` |
| 6 | Topic honestly arguable both ways; debate question present | `script.md` |
| 7 | Archival receipt on screen + source credit on screen | contact sheet, `build_spec.json` |
| 8 | Hard cuts ≤1.2 per 10s (target 0.5–1) | `measure.json` |
| 9 | Captions ≤2 lines, readable, inside safe area, no overlaps | `safezone_check.jpg`, contact sheet |
| 10 | Thud present, unchanged look, deadpan; verdict undersells; loops to frame 1 | contact sheet, last frames |
| 11 | Episode stands alone (no "part 2") | `script.md` |
| 12 | Soft CTA only, in the description | `script.md` |
| 13 | Visibly different from the previous episode (≥2 changes listed) | `strategist_notes.md`, previous spec |
| 14 | Verifier VERDICT is PASS; every image shown is CLEARED | `verification.md`, `assets.csv` |
| 15 | No graphic images; joke never at victims | contact sheet, `script.md` |
| 16 | $0: no point-spending AiToEarn tool was called | `LOG.md` |

## 2. Quality Critic score (1–10) → in `conformance.md`
"Would a good human history creator be proud to post this?" Score it, with reasons:
- Is the hook genuinely intriguing, or just a fact?
- Does the image actually show what the words say?
- Does it feel generic, robotic or templated? Any AI clichés ("Did you know", "fascinating")?
- Typos, awkward line breaks, captions flashing too fast?
- Does Thud's deadpan land, or is he just decoration?
Compare against the real top videos in
`/Users/michaeljara/content-research/research_v2/raw/history/deepdive_codebook.md`.
**7 or more is required to approve.**

## 3. Platform policy check (YouTube Shorts first) [platform, training — re-verify]
- **Inauthentic / mass-produced content:** templated videos with little variation aren't
  monetizable → item 13 matters.
- **Reused content:** only our own render + public-domain/CC0/CC BY images. Never other creators'
  clips.
- **Altered or synthetic content disclosure:** YouTube asks for it when realistic content could be
  mistaken for real. A cartoon stone on real archival images isn't realistic synthetic media, but
  house rule (content-house `CLAUDE.md`) says turn the AI label on whenever the platform offers it.
- **Made for kids:** animated characters are one of YouTube's "made for kids" signals. Thud's
  Archive is general-audience history: set audience to "not made for kids" and make sure tone and
  topics aren't aimed at children.
- **Graphic / violent history:** may be age-restricted or limited even when allowed.
- **Misleading claims:** every on-screen claim matches `verification.md`.

## 4. Verdict (top of `conformance.md`)
- `APPROVE` — every checklist item PASS and quality ≥7.
- `FIX → <role>: <exact changes>` — send back to the Writer, Researcher, Strategist or Editor.
  Max 2 fix rounds per episode; after that, `FAIL` with reasons (logged, not posted).
- `VETO: <reason>` — a hard rule was broken. Not posted.

## 5. Interventions log → `INTERVENTIONS.md`
Make sure every human touch is in the table (add any you find in `LOG.md` that are missing):
```
| # | Step | What a human did / would have had to do | Why the agents couldn't | Could this be automated? How? |
```
Count: questions asked, permission pop-ups, manual fixes, restarts after a usage limit, the
go/no-go answer. A step that needed none of these is "fully autonomous".
