---
name: house-rules
description: Shared rules for every agent in the Thud content house (format, hard rules, files, how to report back). Preloaded by each agent; the Showrunner reads it at the start of /make-episode.
user-invocable: false
---

# House rules — Thud's Archive

## What we make
**Thud's Archive** — numbered YouTube Shorts (later TikTok / Reels) where **Thud**, a deadpan
creature made of stacked stones, presents a history oddity: *two things that were true at the same
time* (e.g. "Cleopatra lived closer to the Moon landing than to the building of the Great Pyramid").
Every episode stands alone. Budget: **$0** (everything is drawn and edited locally).

## Sources of truth (read when your task needs them; cite by path)
- `/Users/michaeljara/content-research/research_v2/I_final_playbook.md` — the verdict and recipe
- `/Users/michaeljara/content-research/research_v2/D_format_anatomy.md` — measured pacing
- `/Users/michaeljara/content-research/research_v2/E_topics.md` — topic backlog (history = section A, lines 8–84)
- `/Users/michaeljara/content-research/research_v2/raw/history/deepdive_codebook.md` — real top videos, coded
- `/Users/michaeljara/content-research/research_v2/H_audience.md` — what commenters actually say
- `/Users/michaeljara/content-formula-research/CONTENT_FORMULA.md` — Thud's design and comedy (Parts 1, 3–6)
- `/Users/michaeljara/content-house/tools/README.md` — the video tools and the build_spec format

## The format (every episode)
| Element | Rule | Why |
|---|---|---|
| Length | 15–30s, aim ~20s | [measured] top history median 15s, bottom 117s |
| Title card | Pinned at top the whole video, ≤6 words, states the overlap | [measured, CONTENT_FORMULA] hook + sound-off safety net |
| Hook 0–3s | First caption = a specific named thing + an unresolved contrast. Never a greeting, never "Did you know" | [measured] |
| Beats | name the thing → mechanism → one concrete number/date → overlap payoff → Thud's verdict | [measured] |
| Verdict | Stamp that undersells ("Noted." "Filed." "Fine, then." "Works." "Sure."), then the video fades back into frame 1 so it loops | [CONTENT_FORMULA] |
| Thud | Lower-left (sometimes lower-right), above the app buttons. Eyes only: blink, glance, half-blink. Never speaks (no mouth) | [CONTENT_FORMULA] |
| Visuals | Real public-domain archival photo / painting / map / document, slow pan or zoom, about 0.5–1 hard cut per 10s. No AI-generated images or video | [measured] |
| Text | Word-by-word captions (current word amber), ≤2 lines, ≤20 characters/second, on-screen source credit. Works fully on mute | [measured] 23–33% of top videos are silent |
| Sound | Silent track + one synthesized stone "thud" on the verdict. Music only if public-domain recording or CC0 with license logged | [measured] voice anxiety is about the voice |
| Topic | Honestly arguable both ways (comments become a debate). Joke at the absurd overlap, never at victims. No graphic images | [measured] top thread was a 2-sided argument |
| Series | Numbered `#NNN`, Thud identical every time, each episode visibly different in images/grade/pacing | [measured] series episodes ~100x one-offs; YouTube demonetizes templated "inauthentic content" [platform, training] |
| CTA | Soft, in the description only (follow / which side are you on?) | [measured] no evidence for keyword CTAs |

Thud's look is fixed by `tools/thud.py` (stacked slate stones, amber seams, amber half-moon eyes,
no mouth, soft shading, **no black outlines** — deliberately different from thick-outline 2D cartoon
styles). Nobody changes it without the founders.

## Hard rules (the Watchdog vetoes any break)
1. **$0.** Never call an AiToEarn tool that spends points (`generate_video`, `generate_image`,
   `asr_subtitles`, `media_understanding`, `image_edit`, etc.). Never buy, recharge or sign up.
2. **Facts:** every claim has 2+ independent sources; every proper noun, date and number re-checked
   (lesson: Whisper wrote "Hamida John Dooby" for **Hamida Djandoubi**).
3. **Licenses:** every image/sound has source URL + license in `assets.csv`. No license = not used.
   Allowed: public domain, CC0, CC BY (with credit). **Avoid CC BY-SA, anything NC or ND, "fair use".**
4. No franchise characters, logos, celebrity or real-person likeness, cloned voices.
5. No health, money or legal advice ("you should…"). History framing only.
6. Never download, repost or remix another creator's video. No fake engagement of any kind
   (bots, bought views/followers, engagement pods, fake accounts).
7. Never print, save or commit API keys or tokens.
8. Only the Showrunner (main session) talks to AiToEarn, and only posts after the Watchdog approves
   **and** Michael says yes.
9. All new files go inside `/Users/michaeljara/content-house/production/`.

## Knowledge tags (use them when you state a fact about platforms or audiences)
- **[measured]** — from the founders' research, cite the file
- **[platform, training — re-verify]** — what TikTok / YouTube / Meta said publicly, as learned in
  training; numbers and policies change, so treat as possibly outdated
- **[practitioner, training]** — common creator practice, not confirmed by the platform

## Files (one folder per episode)
`production/epNNN/` holds: `STATE.md`, `LOG.md`, `topics.md`, `research.md`, `assets/` (+ `assets.csv`),
`verification.md`, `script.md`, `build_spec.json`, `strategist_notes.md`, `final.mp4`, `cover.jpg`,
`render_report.json`, `measure.json`, `contact_sheet.jpg`, `safezone_check.jpg`, `editor_notes.md`,
`conformance.md`, `package.md`, `GO_NO_GO.md` or `HUMAN_ACTION_NEEDED.md`, `publish.md`,
`INTERVENTIONS.md`, `AUTONOMY_REPORT.md`.
Series-wide: `production/SERIES_BIBLE.md`, `production/EPISODES.md` (index of every episode).

## How every agent works
- **Decide, don't ask.** Make the most reasonable choice, write it in your output file with a
  one-line reason, keep going. You cannot ask Michael anything; only the Showrunner can.
- Read inputs from files; write outputs to files. Don't paste big content into your reply.
- **Reply in ≤150 words:** `STATUS: DONE | PUSHBACK | BLOCKED`, files written, key decisions,
  anything the next agent must know. If BLOCKED, say exactly what would unblock it.
- If you hit something a human must do (a login, a payment, a missing account), say so in your
  reply; the Showrunner logs it in `INTERVENTIONS.md`.
