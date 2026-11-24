# Thud Content House — the specialist roster

Picked by Michael on 2026-11-23: **all 32 specialists.** They arrive in waves. The MVP runs with
the 7 core agents; the other 25 specialists' key rules are already folded into those 7 (column
"Lives in now"), and each one becomes its own agent in its wave.

Knowledge tags used in every skill: **[measured]** = your research · **[platform, training —
re-verify]** = what TikTok/YouTube/Meta said publicly, as Claude learned it (can be outdated) ·
**[practitioner, training]** = common creator practice, not platform-confirmed.

```
                         SHOWRUNNER (you type /make-episode)
                                     |
   ┌──────────────┬──────────────┬───┴──────────┬───────────────┬───────────────┐
 STORY ROOM     TRUTH         PRODUCTION     PLATFORMS        INTELLIGENCE     OVERSIGHT
 Head Writer    Researcher    Strategist     YouTube Shorts   Audience Intel   Watchdog (veto)
 Hook Spec.     Verifier      Art Director   TikTok           Competitive      Quality Critic
 Character Dir  Sensitivity   Motion Editor  Instagram Reels  Social Listening Autonomy Auditor
 Script Doctor                Pipeline Eng.  Distribution     Experiment Des.
 Topic Scout                  Asset Libr.    Expansion        Policy Radar
 Format Lab                                  SEO · Localization
                                             Monetization · Account Health
```
Only the Showrunner dispatches agents (Claude Code agents can't start other agents), max 2 at
once. Only the Showrunner talks to AiToEarn.

## MVP — the 7 core agents (built, in `.claude/agents/` + `.claude/skills/`)
| Agent | Job | Lives in now (folded specialists) |
|---|---|---|
| **Showrunner** (`/make-episode`) | Runs the pipeline, decides + logs, go/no-go, posts via AiToEarn, writes the Autonomy Report | Distribution & Community, YouTube Shorts Specialist, Account Health |
| **Researcher** | Picks the best-sourced topic, facts with 2+ independent sources, public-domain images with licenses | Topic & Trend Scout, Archival Researcher, Asset Librarian |
| **Writer** | Series bible, topics, script: hooks, title card, captions, Thud's acting, verdict, title | Head Writer, Hook Specialist, Script Doctor, Character & Comedy Director, SEO |
| **Strategist** | Script → `build_spec.json` (the exact recipe), pushes back, plans variety | Production Strategist, Art Director |
| **Verifier** (veto) | Every fact, name, date, license; sensitivity checklist | Verifier & Rights Clearance, Sensitivity Reader |
| **Editor** | Renders with `tools/`, measures, looks at frames, fixes framing/timing | Motion Editor & Sound, (Pipeline Engineer built the tools already) |
| **Watchdog** (veto) | 16-point checklist, quality score ≥7, platform policy, $0 check, interventions log | Watchdog, Quality Critic, Autonomy Auditor (logging) |

## Wave 2 — "Look better" (3 videos per run, each visibly different)
| Specialist | What they add | Knowledge outline |
|---|---|---|
| Hook Specialist | 10 hooks per episode, scored; title card; first frame; re-hook; loop seam | hook rubric; measured hooks; biggest drop in 0–3s; YouTube "viewed vs swiped away" [platform]; rewatches help [practitioner] |
| Script Doctor | Cut ~20%, payoff ≤8 words, punch word last, reading speed | subtitle norm ~17–20 chars/sec [practitioner]; AI-cliché kill list |
| Character & Comedy Director | Thud's acting per beat, verdict rotation, consistency, lugan3d divergence | CONTENT_FORMULA Parts 4 + 6: deadpan gap, inevitable escalation, undersell |
| Art Director | Brand system, variety rules, cover design, safe-zone overlays | OFL fonts, slate/amber/sepia palette, 3:4 center-safe covers for Instagram grid [platform] |
| Quality Critic | Separate "would a good creator post this?" gate | anti-slop checklist; compare to `deepdive_codebook.md` top stratum |
| Asset Librarian | Library-wide `assets.csv`, dedupe by hash, reuse limits | credit line format (title/author/source/license) |
| Pipeline Engineer | Maintains and tests `tools/`; adds features the Editor asks for; scheduling | render/measure/fetch tools, tests in `tools/test/` |
| Autonomy Auditor & Retro | Times every step, classifies interventions, proposes skill updates as diffs | intervention taxonomy; impact × effort ranking |
| Sensitivity Reader (on-call) | Dark-history review: victims, graphic images, tone | YouTube allows educational violent history but may age-restrict [platform] |

## Wave 3 — "Post everywhere, daily"
| Specialist | What they add | Knowledge outline [platform, training — re-verify] |
|---|---|---|
| YouTube Shorts Specialist | Owns the YouTube package and settings | Shorts up to 3 min; views = every play since Mar 2025, "engaged views" for money; YPP 1K subs + 10M Shorts views/90 days; inauthentic-content policy; made-for-kids signals; private uploads for unverified API apps |
| TikTok Specialist | TikTok package + For-You fit | small test batch then expansion on completion/rewatch/shares; For-You ineligibility (graphic, unoriginal, watermarks); TikTok search reads on-screen text/caption/speech; AI label + C2PA; Creator Rewards needs >1 min; unaudited API apps post private |
| Instagram Reels Specialist | Reels package | Reels up to 3 min; top signals watch time, likes/reach, sends/reach; originality (no other-app watermarks); Trial Reels; 3:4 grid covers |
| Distribution & Community | Cross-post order, schedule, pinned debate comment, replies, moderation | YouTube first [measured]; test 5/week [measured]; thank corrections, pin fixes, never argue |
| Search & SEO | Keyword brief per episode | YouTube autocomplete, Wikipedia pageviews; TikTok Creator Search Insights needs app login (human-only) |
| Policy Radar | Re-checks platform policy pages each run → `POLICY_LOG.md` | keeps the "re-verify" facts fresh |
| Account Health & Security | Account status, strikes, 2FA reminders, recovery plan | YouTube 3 strikes in 90 days = channel removed; never handles passwords |
| + | Connect TikTok + Instagram in AiToEarn; a scheduled task runs `/make-episode` daily | |

## Wave 4 — "Grow and earn"
| Specialist | What they add | Knowledge outline |
|---|---|---|
| Audience Intelligence | Pre-post cold-viewer panel (3 personas, labeled simulation); post-post metrics at 1h/24h/72h/7d; CONTINUE ≥0.5 / CHANGE 0.15–0.5 / STOP <0.15 views per follower [measured] | AiToEarn `get_publish_plan_performance` |
| Competitive Intelligence | Tracks history-niche channels from `C_creators.csv` with the existing research tools | medians, never best video [measured lesson] |
| Social Listening | Mines comments for topics, debates, corrections | "part 2" asked 0 times in 3,408 comments [measured] |
| Experiment Designer | One-variable tests, pre-set thresholds | 30-day plan from `I_final_playbook.md` §6 |
| Topic & Trend Scout | Scored backlog, anniversaries, pageviews | Wikipedia pageviews API, Google Trends, autocomplete |
| Format Lab | New formats to test | 60s+ "Lane L" for TikTok Creator Rewards; photo carousels; "guess the year" |
| Localization | Spanish versions: swap text, re-render, near $0 | Spanish runs ~20–30% longer → re-check timing |
| Expansion Platforms | Facebook, Threads, X, Pinterest, Snapchat | AiToEarn has publish flows for Facebook, Threads, X, Pinterest, LinkedIn |
| Monetization Strategist | Path to money per platform | YPP, Creator Rewards, Facebook Content Monetization [platform, training — re-verify] |

## Deliberately excluded
Bought views/followers, bots, engagement pods, fake accounts, mass follow/DM, reposting other
creators' videos. They break platform rules and risk the accounts.
