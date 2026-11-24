# Content House: Project Notes for Claude

This project automates a short-form video "content house": make videos with AI and post them to TikTok, YouTube Shorts and Instagram Reels, using the AiToEarn MCP server (`aitoearn`).

## Who I'm working with

Michael is a beginner learning to code and build AI agents. Explain what each step does in plain language, and keep explanations short and simple.

## Rules

- **Never publish or post anything without Michael's explicit confirmation**, even if a task seems to call for it.
- **Before generating any video or image, state the model, resolution, length and point cost, and confirm first.** AiToEarn points cost money.
- Prefer the cheapest model that fits (MiniMax H3 at 768p is about 9 points for 5 seconds).
- Only create original content. Do not download, repost or remix other creators' videos (no crawling or drama-recap tools).
- Describe cars and products generically. No real brand names or logos.
- Mark AI-generated videos as AI-generated / synthetic media when the platform allows it.
- Never print, store or commit API keys. No keys go in any file in this folder.
- Save generated videos into this folder with clear names (for example `first-video.mp4`).

## Status

See `SETUP.md` for the setup steps, progress checklist and model prices.

**Agent team (Thud's Archive):** type `/make-episode` to make one history Short with the agent team (see `ROSTER.md`; tools in `tools/`, episodes in `production/`). The run's go/no-go question is Michael's explicit confirmation before anything is posted; it posts unlisted and spends no AiToEarn points.
