# Content House: Setup and Recovery Guide

If anything breaks (new Mac, deleted folder, Claude Code not working), follow these steps to get back to where we were. It takes about 10 minutes.

> 🔐 **No secret keys are stored in this file or this repo, on purpose.** Your AiToEarn API key lives in your private notes and in Claude Code's settings on your Mac, never on GitHub.

## What this project is

- **Claude Code** (on our Claude Pro subscription) is the AI "brain" and harness.
- **AiToEarn** (aitoearn.ai) gives Claude 135 tools to make videos and images and to post to TikTok, YouTube and Instagram.
- Content-house account: the dedicated content Gmail (personal account type).

## Step 1: Install Claude Code

Open a **new** Terminal window (⌘ + Space → Terminal) and run:

```
curl -fsSL https://claude.ai/install.sh | bash
```

Close Terminal, open a new window, and check it worked:

```
claude --version
```

> ⚠️ Do NOT run `export ANTHROPIC_API_KEY=...` in the same Terminal window, or Claude Code may bill API credits instead of using the subscription.

## Step 2: Get the project folder back

If the `content-house` folder is gone, download this repo from GitHub (**Code → Download ZIP**), unzip it, rename the folder to `content-house`, and move it to your home folder (`/Users/michaeljara/content-house`).

Then go into it:

```
cd ~/content-house
```

## Step 3: Get an AiToEarn API key

1. Log in at **aitoearn.ai** (international site, NOT aitoearn.cn) with the content Gmail.
2. Click the 🔑 key icon (bottom left), or Settings → API Key.
3. Create a key and save it in a private note. Never paste it in chats or screenshots.

## Step 4: Connect AiToEarn to Claude Code

In Terminal, inside `~/content-house`, run this. Replace `()` with the key, and delete the parentheses too:

```
claude mcp add --transport http aitoearn https://aitoearn.ai/api/ai/agent/mcp --header "Authorization: Bearer ()"
```

- Check that the line ends with `"` before pressing Enter.
- If you see a `>` prompt afterwards, the closing quote is missing. Press **Control + C** and try again.
- Then run `clear` so the key isn't left on screen.
- If it says the name already exists, first run: `claude mcp remove aitoearn`

> ❌ Don't use the README address `/api/unified/mcp` with `x-api-key`. It failed for us. The address above, from AiToEarn's Claude plugin docs, works.

## Step 5: Start Claude Code and check settings

```
claude
```

Then in Claude Code:

| Setting | Command | Choose |
|---|---|---|
| Model | `/model` | Sonnet |
| Effort | `/effort` | medium |
| Approvals | **Shift + Tab** | "manual mode on" |
| Check AiToEarn | `/mcp` | should show `aitoearn · ✔ connected · 135 tools` |

## Step 6: Test it (free)

```
List my connected AiToEarn channel accounts. Don't generate or publish anything.
```

## Approval rules

- ✅ OK to choose "don't ask again" for tools that only **list / get / check** something.
- ❌ Always approve one at a time for anything that **generates** (spends points) or **publishes** (posts publicly).

## What we've done so far

- [x] Claude Code installed, logged in with Claude Pro
- [x] AiToEarn account created (started with 20 free points)
- [x] AiToEarn connected to Claude Code (135 tools)
- [x] First test video made: MiniMax H3, 768p, 9:16, 5 seconds, 9 points (`first-video.mp4`)
- [ ] Pick the niche with Fabricio (leaning: finance / business / supercars)
- [ ] Create new YouTube, TikTok, Instagram (Business) accounts on the content Gmail and use them normally for a week
- [ ] Design the real video format (15–30s, voiceover, captions, music)
- [ ] Connect the social accounts in AiToEarn (My Channel) and post a first video
- [ ] Build the automatic loop

## Prompt that made the first video

```
Generate ONE 5-second vertical (9:16) video with MiniMax H3 at 768p. Prompt: "Gold coins and stock market charts glowing on screens in a dark modern trading room, camera slowly pushing in, cinematic, dramatic lighting". Use only one generation (about 9 points). When it's done, download the video into this folder as first-video.mp4 and tell me how many points it used. Don't publish anything.
```

## Video model prices (AiToEarn points, checked Nov 21, 2026)

| Model | 5 seconds | 10 seconds |
|---|---|---|
| MiniMax H3 (768p) | 9 | 18 |
| Seedance 2.0 Mini (480p) | 10.7 | 21.4 |
| Seedance 2.0 Fast (480p) | 18.9 | 37.8 |
| Seedance 2.5 (720p) | 102.6 | 205.2 |

## Known harmless issue

"Auto-update failed: no write permission to npm prefix" shows in Claude Code. It's safe to ignore. Don't run any `sudo` command to fix it without checking first.
