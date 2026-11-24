# Video tools (the harness's hands)

Free, local, no AiToEarn points. Python 3.9 + Pillow + ffmpeg (already on this Mac).
Run every command from `~/content-house`.

| Tool | What it does | Command |
|---|---|---|
| `thud.py` | Draws Thud identically every time (poses: idle, blink, half_blink, glance_left, glance_right) | `python3 tools/thud.py --sheet thud_poses.png` |
| `fetch_image.py` | Searches Wikimedia Commons; downloads Commons / Library of Congress images and records license + credit lines in `assets.csv` | `python3 tools/fetch_image.py search "query"` · `... commons "File:X.jpg" --out-dir production/ep001/assets --id img01` · `... loc "<item url>" --out-dir ... --id img02` |
| `render.py` | Turns `build_spec.json` into `final.mp4` + `cover.jpg` + `render_report.json` | `python3 tools/render.py production/ep001/build_spec.json` (`--check` = validate only, `--frames 0,6,18` = preview PNGs) |
| `measure.py` | Checks the finished video (length, size, fps, codec, audio, hard cuts/10s) and makes `contact_sheet.jpg` + `safezone_check.jpg` to look at | `python3 tools/measure.py production/ep001/final.mp4` |

Proof it works: `tools/test/assets_test/test_real.mp4` (made from `spec_real.json` with a
public-domain 1842 painting). `tools/test/thud_poses.png` shows every Thud pose.

## build_spec.json — the exact recipe the Editor renders

All times are seconds. All paths are relative to the spec's own folder (`production/epNNN/`).
Template: `tools/sample_spec.json`.

| Field | Meaning |
|---|---|
| `output`, `cover`, `cover_time` | file names for the video and thumbnail; `cover_time` = which moment becomes the cover (default 0.6s) |
| `duration` | total length, 15–30 |
| `series_tag` | small amber line above the title, e.g. `Thud's Archive · #001` |
| `title_card` | `{text, start, end}` pinned at the top; 6 words max |
| `backgrounds[]` | `{start, end, image, fit, grade, move, transition}` back to back from 0 to `duration`. `fit`: `cover` (fills the screen, pans across) or `contain` (whole picture shown on a blurred backdrop: maps, documents). `grade`: `archival` (sepia), `bw`, `none`. `move`: `{from:{zoom,x,y}, to:{zoom,x,y}}`, zoom ≥1, x/y = 0..1 point of the picture to center on. `transition`: `cut` (default, counts as a hard cut) or `fade` |
| `captions[]` | `{start, end, words[], word_times[]?}` one or two lines each; the current word turns amber. Without `word_times` words are spread by length. Keep ≤20 characters per second; split anything that needs 3 lines |
| `credits[]` | `{text, start, end}` small source credit bottom-right (use `credit_short` from `assets.csv`) |
| `thud` | `{position: lower_left|lower_right, height, track:[{t, pose}]}`; a pose holds until the next one, `blink` lasts 0.15s then returns |
| `verdict` | `{text, start, end, xy?}` the stamp ("Noted.") with a small screen shake |
| `sfx[]` | `{t, type:"thud", volume}` our own synthesized stone thud (put one at the verdict) |
| `music` | `null`, or `{file, license, volume_db}`: only public-domain recordings or CC0, license required |
| `loop` | `{fade_seconds}` the last moment fades into frame 1 so the video loops cleanly |
| `brand` | optional color overrides (keep the defaults for consistency) |

Layout is fixed for safety: all text and Thud stay inside x 60–900, y 200–1440 so TikTok,
Shorts and Reels buttons never cover them.

## Rules for changing these tools
- Run the two test specs after any change: `render.py tools/test/spec_placeholder.json` and
  `render.py tools/test/assets_test/spec_real.json`, then `measure.py` on both outputs.
- Never change Thud's look in `thud.py` without the founders' OK: he must stay identical.
