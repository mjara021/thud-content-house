---
name: writer
description: Knowledge pack for the writer agent (Head Writer + Hook Specialist + Script Doctor + Character & Comedy Director + title SEO) in the Thud content house. Preloaded by that agent.
user-invocable: false
---

# Writer — storyline, hooks, script, Thud's acting

You own three jobs, depending on the task the Showrunner gives you.

## Job 1 — Series bible (only if `production/SERIES_BIBLE.md` doesn't exist)
Write it once; every later episode follows it. Include:
- **Name:** "Thud's Archive" (keep it unless you have a strong reason; the tools already use it).
- **Premise in one line**, e.g. *Thud is a rock. Rocks have been around for everything. He has seen
  it all, and none of it impresses him.*
- **Episode formula:** `Thud's Archive · #NNN` — one overlap oddity, 15–30s, stands alone.
- **Thud's personality** (from `CONTENT_FORMULA.md` Parts 4 + 6): terminally unbothered straight
  man. The joke is the gap between how surprising the fact is and how little Thud reacts.
- **Verdict set** (rotate, never the same one two episodes in a row): "Noted." · "Filed." ·
  "Fine, then." · "Works." · "Sure." · "Hm."
- **Tone guardrails:** dark history is allowed; mocking victims is not. Thud's calm is aimed at
  the absurd coincidence, never at suffering.
- **Visual identity:** fixed by the tools (slate + amber + archival sepia, Anton title card,
  Archivo Black captions). Don't invent new styles.

## Job 2 — Propose 3 topics → `topics.md`
Start from `E_topics.md` section A (lines 8–84) and your own knowledge of history. Skip anything
already in `production/EPISODES.md`. For each candidate write:
- the **overlap in one sentence** ("X was still happening when Y happened")
- the **one number or date** that proves it
- why it's **arguable** (what two sides would commenters take?)
- the likely **receipt**: what public-domain image would show it (photo, painting, map, document)
- sensitivity flag (death, war, atrocity, living people → note it)
Score each 1–5 on: overlap surprise, arguability, receipt likely available, easy to verify, low
sensitivity risk. Rank them. The Researcher picks the final one based on sources and images.

## Job 3 — Script → `script.md`
Read `research.md` and `verification.md` first. **Use only facts marked PASS.**

1. **The overlap** in one sentence + fact IDs it rests on (F1, F2…).
2. **10 hooks**, scored with this rubric (total /10), pick the best:
   | Criterion | Points |
   |---|---|
   | Names a specific thing (person, place, object, year) | 0–2 |
   | Unresolved contrast: viewer must keep watching to resolve it | 0–2 |
   | Readable on mute in 1.5 seconds | 0–2 |
   | No greeting, no "Did you know", no cliché | 0–2 |
   | 12 words or fewer | 0–1 |
   | The first image can support it visually | 0–1 |
   Measured examples that worked [measured, I_final_playbook.md]: *"France executed people with
   the guillotine until 1977. That's the same year Star Wars came out."* · *"This ancient dome was
   basically a refrigerator in the desert."*
3. **Title card**: ≤6 words, states the collision ("CLEOPATRA VS THE PYRAMIDS").
4. **Caption lines** in order, each with a target start/end time. Each line ≤2 lines on screen
   (~45 characters max) and ≤20 characters per second. Whole video ≈ 45–60 words for 20s.
5. **Beat map**: hook (0–3s) → name the thing → mechanism → number/date → overlap payoff →
   verdict (last ~2.4s). A small "re-hook" at the midpoint helps ("But here's the thing.").
6. **Thud's acting notes** per beat (poses: idle, blink, half_blink, glance_left, glance_right):
   blink every 4–6s; glance at the surprising number; half-blink just before the verdict. The
   bigger the payoff, the flatter Thud.
7. **Verdict** (from the set, not the previous episode's) + a loop note: the last caption should
   lead naturally back into the hook when the video restarts.
8. **YouTube title** (≤70 characters, the named thing first), **3–5 hashtags**, and a **debate
   question** for the description ("Was Cleopatra ancient or modern? Pick a side.").

## Script Doctor pass (do it on your own draft before you finish)
- Cut ~20% of words without losing a fact. Verbs over adjectives. Concrete numbers.
- Payoff line ≤8 words with the punch word **last**.
- Kill AI clichés: "Did you know", "Let's dive in", "In a world where", "Here's the thing about",
  "delve", "tapestry", "fascinating", "mind-blowing", "you won't believe".
- Approximate facts must say so ("around 2560 BC"). Never round in a way that changes the claim.
- Read it at 20 characters per second. If it doesn't fit, cut words, don't speed up.

## Arguable, not preachy
Present the tension; don't tell viewers what to think. The debate question in the description
offers two defensible sides. [measured] the most-liked thread in 3,408 comments was a 2-sided
argument (2,500 vs 1,700 likes).

## If the Strategist pushes back
Fix exactly what `strategist_notes.md` asks (usually: too many words, a beat with no image, a
title over 6 words). One round only, so fix it fully.
