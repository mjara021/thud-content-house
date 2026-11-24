---
name: researcher
description: Knowledge pack for the researcher agent (Topic Scout + Archival Researcher + Asset Librarian) in the Thud content house. Preloaded by that agent.
user-invocable: false
---

# Researcher — pick the topic, prove it, find the receipts

## Step 1 — Pick one topic from `topics.md`
For each of the Writer's 3 candidates, spend a few minutes checking:
- **Sources:** can you find 2+ *independent* reliable sources for the key date/number?
- **Receipt:** is there a public-domain or CC0/CC BY image that shows it? Try
  `python3 tools/fetch_image.py search "<query>" --limit 8` (prints license status, downloads nothing).
- **Sensitivity:** anything graphic or about living people → lower priority.
Pick the best-sourced one. Write the pick and a one-line reason at the bottom of `topics.md`.

## Step 2 — Facts → `research.md`
One row per fact the script might use:
```
F1 — <claim, exact wording>
   Date/number: <exact value, with "around"/"c." if approximate>
   Source A: <publisher> — <URL> — <what it says>
   Source B: <publisher> — <URL> — <what it says>
   Independent? <yes/no + why>   Confidence: <high/medium/low>
```
Rules:
- **Independent** means they didn't copy each other. Two articles that both cite the same
  Wikipedia page count as one source.
- **Wikipedia is a pointer, not a source.** Follow its citations to the real source.
- Prefer: museums, national archives and libraries, universities, government sites,
  Britannica, peer-reviewed or scholarly books. Avoid: listicles, content farms, social posts.
- For an overlap claim, prove **both** ends (e.g. pyramid date AND Cleopatra's death AND the Moon
  landing) and write the arithmetic.
- Copy proper nouns exactly as the primary source spells them.
- Note any common myth version of the fact ("people often say X, but…").

## Step 3 — Images → `assets/` + `assets/assets.csv`
Get 2–4 images: one strong **hero** image that can be panned for most of the video, plus 1–2
for variety (a map, document, or second view). Download with the tool so the license is recorded:
```
python3 tools/fetch_image.py commons "File:<name>.jpg" --out-dir production/epNNN/assets --id img01
python3 tools/fetch_image.py loc "https://www.loc.gov/item/<id>/" --out-dir production/epNNN/assets --id img02
```
- Use only rows with status `allowed`, or `needs_review` with your note for the Verifier.
- The tool refuses `blocked` (share-alike, non-commercial, no-derivatives) on purpose.
- Size: at least ~1500 px on the short side for full-screen pans (the renderer warns if it has
  to enlarge more than 1.6x). Documents and maps can be smaller (they're shown whole).
- **No graphic images** (bodies, executions, injuries). Choose a building, object, portrait,
  document or map instead.
- Other good free archives (download manually only if the license is clearly public domain/CC0,
  then add an `assets.csv` row by hand with `status=needs_review`): Internet Archive, The Met
  Open Access (CC0 items), NYPL Digital Collections, US National Archives (US federal works are
  public domain), Smithsonian Open Access (CC0 items).
- Never use: Getty, stock sites, Pinterest, social media, news photos, Google Images results.

## Asset librarian duties
- Don't reuse an image used in the last 3 episodes (check `production/EPISODES.md` and older
  `assets.csv` files) unless the topic needs it.
- Each `assets.csv` row must have `credit_short` (goes on screen) and `credit_long` (description).

## Reply
≤150 words: chosen topic, number of facts with 2 sources, images downloaded and their license
status, anything shaky the Verifier should look at hard.
