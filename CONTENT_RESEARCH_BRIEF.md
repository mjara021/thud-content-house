# Content House: Master Research Brief for an Agent Team

**Owners:** Michael & Fabricio · **Written:** November 22, 2026
**How to use:** Give this whole file to the lead agent (Claude Code). The lead splits the work into the workstreams below, runs them as parallel helper agents, checks their work, and writes the final deliverables.

---

## 0. The goal in one sentence

Find out **exactly what short-form videos to make** (niche, format, editing style, topics) so our harness (Claude Code + AiToEarn) can produce and post AI-made videos to TikTok, YouTube Shorts and Instagram Reels **at scale, without looking like templated "AI slop," and with a realistic path to views and money**.

The research must end in something we can **build**: a second-by-second video recipe, a topic list, and a production pipeline, not just observations.

---

## 1. What we already know (don't redo this, build on it)

### 1a. Our situation
- Two beginner founders, no social media experience, 0 followers, no special expertise ("operator-edge: not established").
- Budget: ~10 hrs/week each, $50–200/month. US, English-language.
- **Production stack:** Claude Code (Claude Pro plan) + AiToEarn MCP (135 tools: AI video generation, AI image generation, voice, subtitles/ASR, timeline editing, publishing to TikTok/YouTube/Instagram and more).
- **Known costs:** AiToEarn's cheapest video model (MiniMax H3, 768p) = ~9 points per 5-second clip, measured on a real generation. The dollar price of a point is still unknown and must be checked.
- AiToEarn posts to TikTok through **TikTok's official Content Posting API** (`open.tiktokapis.com/v2/post/publish`), confirmed by reading its source code. TikTok keeps posts from unaudited apps **private** until the app passes an audit.

### 1b. From two previous depth-engine research runs
- YouTube Shorts ad revenue: 1,000 subs + 10M qualified Shorts views/90 days, rising to **20M from Feb 1, 2027**.
- TikTok Creator Rewards: 10,000 followers + 100K views/30 days, and only videos **over 1 minute** earn.
- Instagram: no reachable view-based payout; early money = brand deals, affiliates, own products.
- Labeling content as AI costs ~7–8% of likes; AI voice costs ~7% of shares (peer-reviewed).
- YouTube's July 2026 "inauthentic content" rules demonetize **generic, repetitive, template-based** AI content and **AI personas presenting as experts on sensitive topics (health, finance)**. AI itself is not banned.
- TikTok's ranking tests each video on its own; follower count is not a direct ranking factor, so new accounts can break out.
- Previous verdict: **GO-TO-TEST on "serialized micro-horror with a named recurring character."** Treat it as a **benchmark to beat**, not the answer.

### 1c. The reference set: 14 videos we picked as the style we want
A Gemini analysis broke these down. **Workstream A must re-watch and re-measure them; don't just trust the summary.**

| # | Video / creator | Platform · length | Style |
|---|---|---|---|
| 1 | CLM-8B explainer (Prompt Engineering) | YT Shorts · 1:04 | AI research explainer |
| 2 | How Persia Made Ice in the Desert (Wilder Ages) | YT Shorts · 1:13 | History mini-doc |
| 3 | Your Vibe-Coded App Can Get Sued (@hayderdotdev) | TikTok/IG · 1:03 | Faceless legal-risk explainer |
| 4 | Anthropic Engineer's 10-Min Claude Code Setup (Nick Saraev) | TikTok/IG · 0:26 | Ultra-tight summary |
| 5 | Run a 2.8T model on a 4GB GPU (Alex Chen) | TikTok/IG · 0:36 | Faceless papercraft explainer |
| 6 | 4 Ways to Aim Higher With AI (Nathan Hodgson) | TikTok/IG · 0:57 | Framework breakdown, split-screen |
| 7 | How to Learn ML Security (Remon) | TikTok/IG · 1:02 | Lo-fi webcam + PNG overlays |
| 8 | Agent Reach (Duncan, AI Automation) | TikTok/IG · 0:53 | Tool showcase + community pitch |
| 9 | The Getty (Brief X) | TikTok · 0:59 | Faceless Google Earth flyover |
| 10 | 5 Claude Code Plugins (@petergriffin.ai) | IG Reels · 1:08 | AI-voiced cartoon dialogue + gameplay |
| 11 | How I Edit Reels With Claude Code (@aidendjohnston) | IG Reels · 1:05 | Builder behind-the-scenes |
| 12 | AI Mind Viruses (@wetclaude) | IG Reels · 2:26 | Conversational deep dive |
| 13 | Anthropic Gave Claude No Eyes (@build.ryanip) | IG Reels · 0:22 | Ultra-compressed tool pitch |
| 14 | GB-115 Anxiety (@captain_biobro) | TikTok · 0:28 | Study notes + meme inserts |

**Patterns Gemini claims (hypotheses to test, not facts):**
- H1. Hooks open with a claim, paradox or "receipt" in the first 2 seconds, never a greeting. Four hook types: borrowed authority, impossible contrast, pain point + fix, identity callout.
- H2. "Receipts replace B-roll": real proof on screen (GitHub stars, terminal, documents, studies) beats generic stock footage.
- H3. The screen changes every 2–4 seconds (cut, insert, overlay, sound effect).
- H4. Split-screen (person or cartoon or gameplay + UI/graphics) is the dominant tech format.
- H5. A persistent top banner or numbered structure lets people follow on mute.
- H6. Admitting a flaw ("the catch: it's slow") increases trust.
- H7. Longer clips survive with a mid-video re-hook ("but ice made in January still had to survive July").
- H8. The CTA matches the goal: comment-keyword = comments/reach, dense lists = saves, humor = shares, problem-only = bio clicks.
- H9. 11 of 14 references are AI/dev-tools/tech, so this may be our niche, or just what we happen to watch.

**Important observation for the automation question:** most of the reference set is built on *receipts* (screen recordings, web pages, documents, diagrams, text animation), **not** AI-generated cinematic video. Reference #11 even built its own pipeline with Claude Code + WhisperX + Python captions + Playwright. Receipts-style videos may be **more automatable and cheaper** with code (screenshots, screen recordings, motion graphics, captions) than with AI video generation. Workstream G must test this.

---

## 2. Research questions

1. **Niches:** Which niches are growing on short-form right now, have room for new accounts, fit a faceless/AI production model, and can make money?
2. **Formats:** Within the winning niches, which exact formats (structure + visuals + audio + length) get the strongest results, especially for **small and new accounts**?
3. **Editing anatomy:** Exactly how are winning videos edited, second by second? (Section 4 defines what to measure.)
4. **Topics:** What specific video topics should we make first, and where do we keep finding new ones?
5. **Automation:** For each winning format, which parts can our harness produce automatically, at what cost and quality, and what still needs a human?
6. **Risk:** Which formats risk demonetization, takedowns, IP problems or bans?
7. **Money:** For each format and niche, what's the realistic path to revenue (brand deals, affiliates, own product, platform payouts)?

---

## 3. The team: 9 workstreams

The lead runs A–H in parallel where possible; I runs last. Each workstream writes its findings to its own file (Section 7).

### A. Reference deconstruction (the 14 videos)
- Re-watch all 14 and fill the **Video Codebook** (Section 4) for each, time-coded.
- Record each video's **public numbers** (views, likes, comments, shares, saves, post date, creator follower count) and compute ratios (Section 5).
- Confirm or reject Gemini's hypotheses H1–H9 with evidence.
- Answer: what do these 14 have in common that we could reproduce **without** a human on camera?
- Flag which references rely on things we don't have (a real person's credibility, an existing audience, a famous character's IP).

### B. Niche discovery & sizing
- Build a long list of **15–20 candidate niches**: include tech/AI tools, developer culture, history mini-docs, places/travel flyovers, science explainers, money/business stories, legal/"hidden rules" explainers, health/biohacking (high risk, see F), micro-horror (previous winner), and any others with strong current growth.
- For each niche, gather: signs of demand (search interest, hashtag volume, view counts on top recent posts), **saturation** (how many active accounts, how similar they look), **small-account breakouts** (accounts under 50K followers with videos far above their follower count), monetization (sponsors and affiliate programs active in the niche), and AI-production fit.
- Shortlist the **top 5–6 niches** with a scored table and reasons.

### C. Creator benchmarking
- In each shortlisted niche, select **5–6 creators** across all 3 platforms:
  - at least 2 **small/fast-growing** accounts (under 50K followers),
  - at least 1 **faceless** and 1 **character-based** account if they exist,
  - at least 1 account that appears to use **AI visuals or AI voice**,
  - active in the last 90 days.
- For each creator, pull their **last 15–30 posts** (not just their best ones) to get typical performance: median views, top views, views-to-followers, posting frequency, and engagement ratios.
- Then pick **10 videos per creator for deep analysis: their 5 best and 5 most recent**, which guards against survivorship bias.
- Note any accounts that tried a format and **stalled or died**: format, how long they posted, what happened.

### D. Format & editing anatomy
- Apply the **Video Codebook** (Section 4) to the deep-analysis videos from C.
- Produce, per niche and overall:
  - average and range for **cuts per 10 seconds**, **visual changes per 10 seconds**, length, words per minute,
  - the most common **hook types**, **structures**, **visual types**, **caption styles**, **audio choices**, **CTAs**,
  - which of these are associated with **higher views-to-followers and share/save rates** (note correlation ≠ causation).
- Build a **second-by-second timing template** for each of the top formats (e.g., 0–2s hook, 2–5s setup, re-hook at ~50%, payoff, CTA).

### E. Topic & idea mining
- For each shortlisted niche, find **where topics come from** and how fresh they need to be: news, GitHub trending, Product Hunt, Reddit, X, research papers, history archives, Google Trends, comments.
- Mine the **comments** of top videos for questions people keep asking ("part 2?", "how do I…", "what tool is this?"). Those are free video ideas.
- Note which topics are **evergreen** (always work) vs **timely** (must be posted within days).
- Output **at least 30 specific video topic ideas per top-3 niche**, each with a hook line and why it should work.

### F. Policy, IP & risk
Check the current written rules (YouTube, TikTok, Instagram) and recent enforcement for each candidate format:
- **AI labeling** requirements on all 3 platforms, and how the label affects reach.
- YouTube **inauthentic / repetitive / templated content** rules: how to make a templated pipeline produce videos that are clearly **not** "near-identical."
- **Copyrighted characters and voice cloning:** e.g. AI-voiced Peter Griffin/Stewie (reference #10). Studios have forced takedowns of AI videos using their characters. **Rate as high-risk; we will NOT use real franchise characters or cloned real voices.** Research an **original** character alternative.
- **Health & supplements** (reference #14): disease/treatment claims are restricted; TikTok's new branded content policy puts supplements in a restricted tier. Rate the risk.
- **Using other creators' content as "receipts"** (screenshots of X posts, GitHub pages, papers): what is fair to show, what needs credit.
- **Gameplay/background footage** (e.g. Minecraft parkour): licensing and "reused content" risk.
- **Automated posting & comment automation:** Instagram comment-to-DM tools (e.g. ManyChat) use Meta's approved API; TikTok has no general comment-to-DM. Confirm what's allowed on each platform.
- **TikTok app audit:** what AiToEarn's TikTok posting needs before videos can be public.
- Output a **risk register**: each risk, how likely, how bad, how to avoid it.

### G. AI production feasibility & cost
For each top format from D, break the video into components and score how our harness can make each one:

| Component | Options to evaluate |
|---|---|
| Research & fact-check | Claude web research with sources |
| Script & hook | Claude |
| Voiceover | AiToEarn/AI voice, or a human voice (cost vs ~7% share penalty) |
| Visuals: "receipts" | Automated screenshots/screen recordings (e.g. Playwright), documents, charts |
| Visuals: motion graphics | Code-based animation (e.g. Remotion or similar), text animation, diagrams |
| Visuals: AI generated | AiToEarn video/image models (cost per clip) |
| Visuals: maps/places | Map/3D flyover sources and their usage rules |
| Recurring character | Can AI keep an **original** character consistent across videos? |
| Captions | AiToEarn ASR subtitles or WhisperX-style word timing |
| Editing & assembly | AiToEarn timeline tools vs ffmpeg/code |
| Music & SFX | Licensed/royalty-free sources and platform music libraries |
| Posting | AiToEarn publishing (official APIs) |

For each format: estimated **cost per video**, **human minutes per video**, **quality risk** ("does it look like slop?"), and **how much variety** the pipeline can produce. Compare "AI-generated video" vs "receipts + motion graphics" pipelines head to head.

**Must also:** look up the current dollar price of AiToEarn points (Recharge page) and the point cost of image, voice and subtitle tools, not just video.

### H. Audience & comments
- Analyze comments on the deep-analysis videos: what makes people comment, share and save; complaints; requests.
- Specifically capture **audience reactions to AI-made content** (positive, negative, indifferent) by niche.
- Identify **what the audience wants more of** in each niche.

### I. Synthesis & red team (runs last)
- Combine A–H. Score every candidate format on **works × automatable × cheap × safe × monetizable** (Section 6).
- A red-team agent then tries to **break** the top pick: argue it won't work, find counter-evidence, look for survivorship bias, check every key number against its source.
- Compare the top pick against the previous benchmark (serialized micro-horror) and say which is better for us and why.

---

## 4. The Video Codebook: what to measure in every analyzed video

Record each item with a **timestamp**. Use the exact definitions so different agents measure the same way.

**Basics:** platform, URL, creator, follower count, post date, length (seconds), niche, topic in one sentence.

**Purpose:** entertain / teach / inspire / shock / sell / build community (pick main + secondary).

**Hook (0–3 seconds):**
- First spoken words (exact quote), first on-screen text, first visual.
- Hook type: borrowed authority / impossible contrast / pain point + fix / identity callout / question / shocking number / story in motion / other.
- Is the payoff promised? ("by the end you'll…")

**Structure:** list each beat with timestamps (hook → setup → points → re-hook → payoff → CTA). Structure type: listicle, story arc, problem→solution, before/after, myth vs fact, tutorial, news recap, dialogue, series/part-N. Mid-video re-hook present? Where?

**Pacing (count these precisely):**
- **Cut** = the shot or scene changes. Report **cuts per 10 seconds**.
- **Visual change** = any change on screen: cut, zoom, new overlay/graphic, text appearing, meme insert, transition. Report **visual changes per 10 seconds**.
- Longest time the screen stays the same (seconds).
- Speaking speed (words per minute) and silence/dead air.

**Camera & framing:** shot types used (close-up, medium, screen recording, full-screen graphic, map/3D view); angles (eye-level, top-down, over-shoulder, POV); layout (full-screen, split-screen top/bottom, picture-in-picture, green-screen over content).

**What is on screen (list everything that appears):**
- People? (real face, hands, AI person, cartoon, none)
- "Receipts" (GitHub pages, terminal, documents, studies, tweets, star counts, prices, charts)
- Stock footage / AI-generated footage / gameplay / maps / animation / memes
- **Persistent elements** (top banner, progress bar, numbered steps, logo/watermark)
- How often graphics change and what triggers the change (each new sentence? each new point?)

**Text & captions:** caption style (word-by-word, phrase, full sentence), size, color, position, highlighted keywords, emojis; on-screen headline text; readability on mute.

**Audio:** voice (real / AI / character), tone and energy, music (trending / royalty-free / none), sound effects (whoosh, stamp, ding) and where they land.

**Credibility devices:** specific numbers, sources shown, admitted flaws ("the catch…"), borrowed authority.

**CTA:** exact words, placement (start / middle / end / caption / pinned comment), type (comment keyword, follow for part 2, link in bio, save this, share with a friend).

**Caption/description & hashtags:** length, keywords, number of hashtags.

**Results (public only):** views, likes, comments, shares, saves, plus ratios (Section 5).

**Automation notes:** which parts our harness could make automatically, which need a human, what it would cost.

---

## 5. Metrics and evidence rules

- **Use public numbers only:** views, likes, comments, shares, saves, follower count, post date. Retention, RPM and "qualified views" are creator-only and should be marked **UNAVAILABLE**, never guessed.
- **Ratios to compute** (each divided by views): like rate, comment rate, share rate, save rate. Also **views ÷ followers** (the best "algorithm pushed it" signal for small accounts).
- A "view" is counted differently on each platform; **compare within a platform**, not across them.
- **Typical, not just the best:** always report the **median** of a creator's recent posts, not only their top video.
- **Data collection:** public-data tools such as Apify actors (no-login TikTok/Instagram/YouTube scrapers that export views, likes, comments, shares, saves, followers, captions, hashtags, post dates) or the platforms' own public pages. Only collect **public** data, without logging in or bypassing restrictions, and respect each site's terms. AiToEarn also has browser and crawling tools. Use them **for analysis only, never to download and repost content**.
- **Every claim needs a source link and a date.** Anything unverifiable = **UNAVAILABLE**.
- **Video viewing:** where agents can't watch video directly, use transcripts, frame captures and creator-published breakdowns, and say which method was used.
- **Survivorship bias:** for every winning pattern, look for accounts that used it and failed.

---

## 6. Scoring each candidate format (used by workstream I)

Score 1–5 on each and explain the score:

| Criterion | What 5 looks like |
|---|---|
| **Works** | Small accounts repeatedly get views well above their follower count |
| **Automatable** | Harness makes 80%+ of each video with <15 human minutes |
| **Cheap** | Fits $50–200/month at 4–7 videos per week |
| **Safe** | No IP, health-claim or "templated content" risk; AI label doesn't kill it |
| **Variety** | Pipeline can make 100 videos that don't look the same |
| **Monetizable** | Clear brand-deal, affiliate or product path in this niche |
| **Fits us** | Two beginners can do it without a face, credentials or an existing audience |

---

## 7. Deliverables

Write everything to a `research/` folder:

```
research/
  00_SUMMARY.md              ← plain-language summary for two beginners (read this first)
  A_reference_videos.md      ← 14 references, codebook + hypothesis verdicts
  B_niches.md                ← long list, scored shortlist
  C_creators.csv             ← creator table with numbers and links
  C_videos.csv               ← every analyzed video with codebook fields and ratios
  D_format_anatomy.md        ← pacing stats, patterns, timing templates
  E_topics.md                ← 30+ topic ideas per top-3 niche, with hook lines
  F_risk_register.md         ← policy/IP/health/automation risks and fixes
  G_production.md            ← component-by-component automation plan + cost per video
  H_audience.md              ← comment insights, reactions to AI
  I_final_playbook.md        ← the answer (below)
```

**`I_final_playbook.md` must include:**
1. **The #1 niche + format** to start with, and 2 backups, with scores and reasons.
2. A **second-by-second recipe** for the #1 format: length, hook formula, structure, cuts and visual changes per 10 seconds, layout, caption style, voice, music, CTA.
3. An **original recurring character or brand identity** suggestion (no copyrighted characters).
4. **The first 20 videos to make**: topic, hook line, key "receipts" to show.
5. **The production pipeline:** each step, which tool does it, cost, human time.
6. **A 30-day test plan:** posting schedule (4–7/week), what to measure, and pre-written numbers for continue / change / stop.
7. **Risk checklist** to run before each post.
8. **A GO-TO-TEST / REFRAME / NO-GO verdict** for the #1 format.

---

## 8. Rules for every agent

- Study **patterns**; never copy, download-and-repost, or recreate anyone's actual video.
- **No real franchise characters, celebrity likenesses, or cloned real voices** in our plans.
- **No medical or financial advice** formats that make treatment or "buy this" claims.
- Public data only; respect platform terms; no logging in to scrape.
- Cite sources with dates; mark gaps UNAVAILABLE; don't round up weak evidence.
- Write for **two beginners**: plain language, define any jargon.
- The lead agent checks each workstream's sources before using them, and **asks Michael before spending money** (e.g. paid scraping tools, AiToEarn points for test generations).
