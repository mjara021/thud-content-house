#!/usr/bin/env python3
"""Find and download archival images WITH their license recorded.

Search Wikimedia Commons (prints candidates, downloads nothing):
    python3 tools/fetch_image.py search "great pyramid giza 19th century" --limit 8

Download one Commons file into an episode's assets folder:
    python3 tools/fetch_image.py commons "File:Some_photo.jpg" --out-dir production/ep001/assets --id img01

Download one Library of Congress item:
    python3 tools/fetch_image.py loc "https://www.loc.gov/item/2002712345/" --out-dir production/ep001/assets --id img02

Add --dry-run to see the license info without downloading.

Every download appends a row to <out-dir>/assets.csv with source, author, license,
status, and ready-made credit lines. Status is one of:
  allowed       public domain, CC0, or CC BY (credit required)
  blocked       share-alike (SA), non-commercial (NC), no-derivatives (ND), fair use, or copyrighted
  needs_review  anything unclear (e.g. LOC "no known restrictions"): the Verifier must decide
House rule: only "allowed" (or "needs_review" that the Verifier clears in writing) may be used.
Python 3.9 compatible. Standard library only.
"""
import argparse
import csv
import datetime
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request

UA = "ThudContentHouse/0.1 (educational short-video research script)"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
MAX_BYTES = 25 * 1024 * 1024
FIELDS = ["asset_id", "file", "source", "source_page", "download_url", "title", "author", "license",
          "license_url", "status", "credit_short", "credit_long", "width", "height", "sha256", "fetched_at", "notes"]


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise SystemExit("file larger than 25 MB, refusing: " + url)
        ctype = r.headers.get("Content-Type", "")
    return (data, ctype) if binary else json.loads(data.decode("utf-8"))


def strip_html(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", s).strip()


def classify(license_name, copyrighted=None, restrictions=""):
    l = (license_name or "").lower()
    tokens = set(re.split(r"[\s\-_/.,()]+", l))
    if "nc" in tokens or "nd" in tokens or "fair" in tokens or "non-free" in l:
        return "blocked", "non-commercial / no-derivatives / fair-use license"
    if "sa" in tokens:
        return "blocked", "share-alike (SA) license: house rule avoids it"
    if restrictions:
        return "needs_review", "extra restrictions: " + restrictions
    if "cc0" in tokens or "public domain" in l or l.startswith("pd") or copyrighted == "False":
        return "allowed", "public domain / CC0"
    if "by" in tokens and "cc" in tokens:
        return "allowed", "CC BY: credit required"
    return "needs_review", "license not recognised: " + (license_name or "none given")


def commons_info(titles, thumb_width=3000):
    q = {"action": "query", "format": "json", "prop": "imageinfo", "titles": "|".join(titles),
         "iiprop": "url|size|mime|extmetadata", "iiurlwidth": str(thumb_width)}
    data = get(COMMONS_API + "?" + urllib.parse.urlencode(q))
    out = []
    for page in (data.get("query", {}).get("pages", {}) or {}).values():
        if "imageinfo" not in page:
            continue
        ii = page["imageinfo"][0]
        md = ii.get("extmetadata", {})
        val = lambda k: (md.get(k) or {}).get("value", "")  # noqa: E731
        lic = val("LicenseShortName")
        status, why = classify(lic, val("Copyrighted"), strip_html(val("Restrictions")))
        title = strip_html(val("ObjectName")) or page["title"].replace("File:", "").rsplit(".", 1)[0]
        author = strip_html(val("Artist")) or "Unknown author"
        lic_short = "public domain" if status == "allowed" and "CC BY" not in lic.upper() else lic
        out.append({
            "title": title, "page_title": page["title"],
            "source_page": ii.get("descriptionurl", ""),
            "download_url": ii.get("thumburl") or ii.get("url"),
            "original_url": ii.get("url"),
            "width": ii.get("thumbwidth") or ii.get("width"), "height": ii.get("thumbheight") or ii.get("height"),
            "original_size": [ii.get("width"), ii.get("height")], "mime": ii.get("mime"),
            "author": author, "license": lic, "license_url": val("LicenseUrl"),
            "date": strip_html(val("DateTimeOriginal")), "status": status, "why": why,
            "credit_short": "Image: %s / Wikimedia Commons (%s)" % (author[:40], lic_short),
            "credit_long": "%s, by %s, %s, via Wikimedia Commons (%s)" % (title, author, lic or "license unknown",
                                                                          ii.get("descriptionurl", "")),
        })
    return out


def cmd_search(a):
    q = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": "6",
         "gsrsearch": "filetype:bitmap " + a.query, "gsrlimit": str(a.limit)}
    data = get(COMMONS_API + "?" + urllib.parse.urlencode(q))
    titles = [p["title"] for p in (data.get("query", {}).get("pages", {}) or {}).values()]
    res = commons_info(titles, thumb_width=400) if titles else []
    for r in res:
        r.pop("download_url", None)
    print(json.dumps(res, indent=2))


def save(info, out_dir, asset_id, source, notes=""):
    os.makedirs(out_dir, exist_ok=True)
    data, ctype = get(info["download_url"], binary=True)
    if not ctype.startswith("image/"):
        raise SystemExit("not an image (%s): %s" % (ctype, info["download_url"]))
    ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/tiff": ".tif", "image/gif": ".gif"}.get(ctype.split(";")[0], ".img")
    fname = asset_id + ext
    with open(os.path.join(out_dir, fname), "wb") as fh:
        fh.write(data)
    row = {
        "asset_id": asset_id, "file": fname, "source": source, "source_page": info.get("source_page", ""),
        "download_url": info["download_url"], "title": info.get("title", ""), "author": info.get("author", ""),
        "license": info.get("license", ""), "license_url": info.get("license_url", ""), "status": info["status"],
        "credit_short": info.get("credit_short", ""), "credit_long": info.get("credit_long", ""),
        "width": info.get("width", ""), "height": info.get("height", ""),
        "sha256": hashlib.sha256(data).hexdigest(),
        "fetched_at": datetime.datetime.now().isoformat(timespec="seconds"), "notes": (info.get("why", "") + " " + notes).strip(),
    }
    csv_path = os.path.join(out_dir, "assets.csv")
    new = not os.path.isfile(csv_path)
    with open(csv_path, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    return row


def cmd_commons(a):
    title = a.file if a.file.startswith("File:") else "File:" + a.file.split("File:")[-1].split("/")[-1]
    res = commons_info([urllib.parse.unquote(title)])
    if not res:
        raise SystemExit("not found on Commons: " + title)
    info = res[0]
    if a.dry_run:
        print(json.dumps(info, indent=2))
        return
    if info["status"] == "blocked" and not a.keep_blocked:
        print(json.dumps(info, indent=2))
        raise SystemExit("BLOCKED license, not downloaded: " + info["why"])
    print(json.dumps(save(info, a.out_dir, a.id, "wikimedia_commons"), indent=2))


def cmd_loc(a):
    url = a.url.split("?")[0].rstrip("/") + "/?fo=json"
    data = get(url)
    item = data.get("item", {}) or {}
    rights = item.get("rights_advisory") or item.get("rights") or ""
    if isinstance(rights, list):
        rights = " ".join(rights)
    best = None
    for res in data.get("resources", []) or []:
        for group in res.get("files", []) or []:
            for f in group if isinstance(group, list) else [group]:
                if f.get("mimetype") == "image/jpeg" and (f.get("width") or 0) <= 4000:
                    if best is None or (f.get("width") or 0) > (best.get("width") or 0):
                        best = f
    if best is None:
        imgs = item.get("image_url") or data.get("image_url") or []
        if imgs:
            best = {"url": imgs[-1]}
    if best is None:
        raise SystemExit("no downloadable JPEG found for " + a.url)
    status = "needs_review"
    why = "LOC rights text: " + (rights or "none given") + " (Verifier must confirm)"
    if re.search(r"copyright|permission required|restricted", rights, re.I) and not re.search(r"no known", rights, re.I):
        status, why = "blocked", "LOC rights text mentions restrictions: " + rights
    title = item.get("title", "") if isinstance(item.get("title", ""), str) else str(item.get("title"))
    creator = item.get("contributor_names") or item.get("creator") or ["Unknown"]
    if isinstance(creator, list):
        creator = "; ".join(creator[:2])
    dl = best["url"] if best["url"].startswith("http") else "https:" + best["url"]
    info = {"title": title, "author": creator, "source_page": a.url, "download_url": dl,
            "license": rights[:200], "license_url": "https://www.loc.gov/legal/", "status": status, "why": why,
            "width": best.get("width", ""), "height": best.get("height", ""),
            "credit_short": "Image: Library of Congress", "credit_long": "%s, %s, Library of Congress (%s)" % (title, creator, a.url)}
    if a.dry_run:
        print(json.dumps(info, indent=2))
        return
    if status == "blocked" and not a.keep_blocked:
        print(json.dumps(info, indent=2))
        raise SystemExit("BLOCKED, not downloaded")
    print(json.dumps(save(info, a.out_dir, a.id, "library_of_congress"), indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Find and download archival images with licenses")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=8)
    for name in ("commons", "loc"):
        p = sub.add_parser(name)
        p.add_argument("file" if name == "commons" else "url")
        p.add_argument("--out-dir", default=".")
        p.add_argument("--id", default="img01")
        p.add_argument("--dry-run", action="store_true")
        p.add_argument("--keep-blocked", action="store_true", help="download even if blocked (for review only)")
    a = ap.parse_args()
    {"search": cmd_search, "commons": cmd_commons, "loc": cmd_loc}[a.cmd](a)
