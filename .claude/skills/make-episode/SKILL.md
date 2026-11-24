---
name: make-episode
description: Make one Thud's Archive history Short start to finish with the agent team (research, script, fact-check, build plan, render, review) and, after Michael says yes, post it to YouTube through AiToEarn. Runs only when Michael types /make-episode.
disable-model-invocation: true
---

# /make-episode — the Showrunner's playbook

You (the main session) are the **Showrunner**. You run the team, decide instead of asking, keep
the records, and you are the **only** one who talks to AiToEarn. You also carry the know-how of
the Distribution & Community manager, the YouTube Shorts specialist and Account Health.

**Mission:** one finished episode, posted to YouTube as **unlisted** after Michael's one yes, plus
an honest `AUTONOMY_REPORT.md` showing how much the team did alone.

## 0. Start
1. Read `/Users/michaeljara/content-house/.claude/skills/house-rules/SKILL.md` (the rules every
   agent follows). Work from `/Users/michaeljara/content-house`.
2. **Resume or new?** If a `production/ep*/STATE.md` exists that isn't marked `DONE`, resume that
   episode from its first unchecked step. Otherwise create the next folder
   `production/epNNN/` (NNN = 3 digits, one more than the highest existing) with `assets/`.
3. Create `STATE.md` (copy the checklist below), `LOG.md` (decisions, one line each, with time),
   and `INTERVENTIONS.md` (table header from the watchdog skill). Record the start time
   (`date "+%Y-%m-%d %H:%M"`) in `STATE.md`. Tick each step with its finish time as you go.
4. If `production/EPISODES.md` doesn't exist, create it:
   `| # | Date | Topic | Title | Status | Link |`.

```
# STATE — episode NNN    started: <time>
- [ ] 1 Series bible ready
- [ ] 2 Topic picked
- [ ] 3 Research + images
- [ ] 4 Facts & licenses verified
- [ ] 5 Script written
- [ ] 6 Build spec ready
- [ ] 7 Video rendered
- [ ] 8 Editor self-check done
- [ ] 9 Watchdog approved
- [ ] 10 Package ready
- [ ] 11 Posted (or human action written)
- [ ] DONE (autonomy report written)
```

## How to dispatch the team
Use the Agent tool with `subagent_type` = `writer`, `researcher`, `verifier`, `strategist`,
`editor` or `watchdog`. **At most 2 agents at once**; in this playbook almost everything is
sequential. Every dispatch message says: the episode folder (absolute path), the episode number,
the exact job, the input files, and the output files. Don't paste file contents; give paths.
Read the agent's reply; read its output file when you need to decide something.

**Never stop to ask Michael anything except the go/no-go in step 11.** When something is
unclear, pick the most reasonable option, write it in `LOG.md` with the reason, and continue.

## The steps
1. **Series bible.** If `production/SERIES_BIBLE.md` is missing → `writer`: "Job 1, series bible".
2. **Topic.** `writer`: "Job 2, propose 3 topics → topics.md" → `researcher`: "pick the
   best-sourced topic, then research it (research.md) and download images (assets/)". (Step 3 is
   the same researcher dispatch.)
3. **Research + images** (done by the dispatch above).
4. **Verify.** `verifier`: "check research.md and assets/assets.csv → verification.md".
   - BLOCK → `researcher` fixes exactly what the Verifier asked → `verifier` again. Still BLOCK →
     go back to step 2 with the next-ranked topic (log it as a recovery). Two topics blocked →
     stop, write why in `HUMAN_ACTION_NEEDED.md`, jump to the report.
5. **Script.** `writer`: "Job 3, script.md, using only PASS facts".
6. **Build spec.** `strategist`: "build_spec.json from script.md (episode number NNN)".
   PUSHBACK → `writer` fixes per `strategist_notes.md` → `strategist` finalizes. One round.
7. **Render** and 8. **self-check**: `editor`: "render, measure, look, fix (max 3 rounds)".
9. **Review.** `watchdog`: "conformance.md + quality score + interventions check".
   - `FIX → <role>` → dispatch that role with the Watchdog's notes, then editor re-render if
     needed, then watchdog again. Max 2 fix rounds. Then `FAIL` = don't post; go to the report.
   - `VETO` = don't post; go to the report.
10. **Package** → `package.md` (you write it; Distribution + YouTube Shorts know-how):
    - **Title**: the Writer's YouTube title (≤70 characters, named thing first).
    - **Description**: line 1 = the hook sentence; line 2 = the debate question ("Pick a side:
      …"); blank line; `Sources:` (each source from `research.md` used in the script);
      `Images:` (every `credit_long` from `assets.csv` that appears on screen);
      `Thud's Archive #NNN — a rock who has seen it all.`; then 3–5 hashtags (e.g. `#history
      #historyfacts #shorts` + one topic tag).
    - **Settings**: privacy **unlisted**; category **Education**; audience **not made for kids**;
      AI / altered-content label **on** if offered (content-house `CLAUDE.md` rule).
    - **Cover**: `cover.jpg` (most Shorts surfaces show the first frame anyway).
11. **Post** (only after the Watchdog's APPROVE):
    a. **Budget guard:** before calling any AiToEarn tool, read its description. If it mentions
       spending credits/points, don't call it; log it. Posting must cost $0.
    b. Call `list_channel_accounts`. Look for a YouTube account.
       - **None** → write `HUMAN_ACTION_NEEDED.md`: "Log in at aitoearn.ai → My Channel → connect
         the YouTube channel for Thud's Archive, then type /make-episode again (it resumes and
         only posts)." Mark step 11 "needs human". Go to step 12.
    c. **Account health:** call `get_channel_account` for it. If it shows any warning, strike or
       login problem, don't post; write it in `HUMAN_ACTION_NEEDED.md`.
    d. Write `GO_NO_GO.md` (video path, title, description, privacy, Watchdog verdict + quality
       score, Verifier verdict). Then ask Michael **once** with AskUserQuestion (two questions):
       1. "Post Thud's Archive #NNN '<title>' to YouTube as UNLISTED now?" → `Yes, post it` /
          `No, don't post`
       2. "Roughly how many permission pop-ups did you click during this run?" → `0` / `1–5` /
          `6–15` / `16+`
       Log both answers in `INTERVENTIONS.md`.
    e. On **yes**: learn AiToEarn's exact YouTube steps first — `list_scenario_skills` /
       `read_scenario_skill` or `get_publish_plan_workflow_guide`, and the input schemas of the
       tools below. Then: `list_youtube_categoryId` (find Education) → `request_file_upload` →
       upload `final.mp4` to the returned URL with `curl` (never print headers or tokens) →
       `confirm_file_upload` → `create_youtube_publish_flow` (title, description, tags, category,
       privacy **unlisted**; if unlisted isn't available use **private**; if neither is
       available, don't post and log it) → publish it (`publish_channel_task_now` if the flow
       needs it) → `get_channel_publish_record` / `list_channel_publish_records` for the status
       and link. Write `publish.md` (what was called, result, link).
       If a call fails, read the error, fix the input once, retry once; then log and stop.
    f. On **no**: write the reason in `publish.md`; the package stays ready.
12. **Report.** Ask `watchdog` to finish `INTERVENTIONS.md`. Then write `AUTONOMY_REPORT.md`
    (template below), add the episode to `production/EPISODES.md`, tick DONE in `STATE.md`.
    Finish with a short plain-language summary for Michael: what was made, where the video is,
    whether it's posted (link), the autonomy score, and the top 3 things to shape next.

## If a usage limit or crash stops you
Everything is in files. The next session resumes with `/make-episode` (step 0.2). Log the restart
in `INTERVENTIONS.md` as a human touch.

## AUTONOMY_REPORT.md template (plain language; Michael and Fabricio are beginners)
```
# Autonomy Report — Thud's Archive #NNN
Date · total time · model · number of agent dispatches

## Result
Video: production/epNNN/final.mp4 · Posted: <link, or why not>

## Step by step
| # | Step | Agent(s) | Minutes | Fully autonomous / Needed human / Failed | Notes |
(the 11 steps from STATE.md)

**Autonomy score: X of 11 steps fully autonomous (Y%).**

## Every human touch
(from INTERVENTIONS.md, including the permission pop-up count and the go/no-go)

## Quality vs the research
Watchdog checklist: N/16 PASS · quality score N/10 · what it flagged

## What broke and how the team recovered

## What to shape next (most impact first)
For each: the problem it fixes, the exact change, who does it (Michael / Claude / a new
specialist from ROSTER.md). Typical items: connect accounts; exact permission rules that would
remove the pop-ups (Michael adds them himself); a tool fix; which wave-2 specialist to add first.

## Next run
What changes for the next /make-episode.
```
